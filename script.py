import argparse
import asyncio
import os
import logging
from typing import List, Tuple, Optional
from dotenv import load_dotenv
import aiohttp
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
from io import BytesIO
import requests
import qrcode
from dataclasses import dataclass
import socket

# Load environment variables
load_dotenv()
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Paths
FONT_DIR = "font/Ubuntu"
SAVE_DIR = "exported_files"

# Social media icon URLs
LINKEDIN_ICON_URL = "https://cdn-icons-png.flaticon.com/512/174/174857.png"
FACEBOOK_ICON_URL = "https://cdn-icons-png.flaticon.com/512/124/124010.png"
LINKEDIN_QR_URL = "https://www.linkedin.com/company/artificialintelligenceimmersion"

@dataclass
class ImageConfig:
    title: str
    subtitle: str
    quality: int
    per_page: int

class ImageModifier:
    def __init__(self, config: ImageConfig):
        self.config = config
        self.linkedin_icon = self._download_icon(LINKEDIN_ICON_URL)
        self.facebook_icon = self._download_icon(FACEBOOK_ICON_URL)
        self.qr_code = self._generate_qr_code(LINKEDIN_QR_URL)
        self.font_small = ImageFont.truetype(os.path.join(FONT_DIR, "Ubuntu-Light.ttf"), 20)

    def _download_icon(self, url: str) -> Image.Image:
        """Download and resize an icon."""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            icon = Image.open(BytesIO(response.content)).convert('RGBA')
            return self._add_icon_background(icon.resize((40, 40)))
        except requests.RequestException as e:
            logger.error(f"Error downloading icon from {url}: {e}")
            return Image.new('RGBA', (40, 40), color=(255, 255, 255, 0))

    def _add_icon_background(self, icon: Image.Image) -> Image.Image:
        """Add a round background to the icon."""
        size = (icon.width + 20, icon.height + 20)
        background = Image.new('RGBA', size, (255, 255, 255, 0))
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size[0], size[1]), fill=255)
        rounded_icon = Image.new('RGBA', size, (0, 0, 0, 0))
        rounded_icon.paste(icon, (10, 10), icon)
        return Image.composite(rounded_icon, background, mask)

    def _generate_qr_code(self, url: str) -> Image.Image:
        """Generate a QR code for a given URL."""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white").convert('RGBA')
        return img.resize((100, 100))

    def add_overlay_and_text(self, image: Image.Image) -> Image.Image:
        # Convert image to RGB mode to avoid transparency issues
        image = image.convert('RGB')
        image = image.filter(ImageFilter.GaussianBlur(radius=2))
        overlay = self._create_gradient_overlay(image.size)
        image = Image.alpha_composite(image.convert('RGBA'), overlay)
        draw = ImageDraw.Draw(image)

        title_font = ImageFont.truetype(os.path.join(FONT_DIR, "Ubuntu-Bold.ttf"), int(image.height * 0.08))
        subtitle_font = ImageFont.truetype(os.path.join(FONT_DIR, "Ubuntu-Light.ttf"), int(image.height * 0.04))

        padding_x, padding_y = int(image.width * 0.05), int(image.height * 0.05)
        title_position = (padding_x, padding_y)
        subtitle_position = (padding_x, padding_y + title_font.getbbox(self.config.title)[3] + 10)

        self._draw_text_with_shadow(draw, title_position, self.config.title, title_font)
        self._draw_text_with_shadow(draw, subtitle_position, self.config.subtitle, subtitle_font)

        self._add_decorative_line(draw, image.size)
        self._add_social_icons(image)
        self._add_qr_code_with_text(image)

        return image

    def _create_gradient_overlay(self, size: Tuple[int, int]) -> Image.Image:
        overlay = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        for i in range(int(size[1] * 0.4)):
            alpha = int(255 * (1 - i / (size[1] * 0.4)))
            draw.line((0, i, size[0], i), fill=(0, 0, 0, alpha))
        return overlay

    def _draw_text_with_shadow(self, draw: ImageDraw, position: Tuple[int, int], text: str, font: ImageFont):
        shadow_color, text_color = (0, 0, 0, 128), (255, 255, 255, 255)
        draw.text((position[0]+2, position[1]+2), text, font=font, fill=shadow_color)
        draw.text(position, text, font=font, fill=text_color)

    def _add_decorative_line(self, draw: ImageDraw, size: Tuple[int, int]):
        line_color, line_width, line_length = "#df3abc", 10, 50
        padding = int(size[1] * 0.05)
        start_point = (size[0] - line_length - padding, size[1] - padding)
        end_point = (size[0] - padding, size[1] - padding)
        draw.line([start_point, end_point], fill=line_color, width=line_width)

    def _add_social_icons(self, image: Image.Image):
        padding = int(image.height * 0.05)
        icon_size = self.linkedin_icon.size[0]
        spacing = 10
        linkedin_position = (padding, image.height - padding - icon_size)
        facebook_position = (padding, linkedin_position[1] - icon_size - spacing)
        image.paste(self.linkedin_icon, linkedin_position, self.linkedin_icon)
        image.paste(self.facebook_icon, facebook_position, self.facebook_icon)

    def _add_qr_code_with_text(self, image: Image.Image):
        padding = int(image.height * 0.05)
        qr_code_position = (image.width - self.qr_code.size[0] - padding, padding)
        image.paste(self.qr_code, qr_code_position, self.qr_code)

        draw = ImageDraw.Draw(image)
        text_position = (qr_code_position[0], qr_code_position[1] + self.qr_code.size[1] + 10)
        draw.text(text_position, "by berg-AI", font=self.font_small, fill=(255, 255, 255, 255))

class UnsplashImageDownloader:
    def __init__(self, config: ImageConfig):
        self.config = config
        os.makedirs(SAVE_DIR, exist_ok=True)
        self.image_modifier = ImageModifier(config)

    async def search_unsplash_images(self) -> List[str]:
        url = "https://api.unsplash.com/search/photos"
        headers = {"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"}
        params = {"query": self.config.title, "per_page": self.config.per_page, "orientation": "landscape"}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, params=params) as response:
                    response.raise_for_status()
                    data = await response.json()
            return [result["urls"]["regular"] for result in data["results"]]
        except aiohttp.ClientError as e:
            logger.error(f"Error fetching images from Unsplash: {e}")
            return []

    async def fetch_and_save_image(self, url: str, idx: int) -> Optional[str]:
        save_path = os.path.join(SAVE_DIR, f"{self.config.title.replace(' ', '_')}_{idx + 1}.png")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    image_data = await response.read()

            image = Image.open(BytesIO(image_data))

            if image.width >= 630 and image.height >= 512:
                modified_image = self.image_modifier.add_overlay_and_text(image)
                modified_image.save(save_path, format='PNG', quality=self.config.quality)
                logger.info(f"Modified image saved to {save_path}")
                return save_path
            else:
                logger.warning(f"Image skipped, resolution too low ({image.width}x{image.height}).")
                return None
        except Exception as e:
            logger.error(f"Error downloading or modifying image: {e}")
            return None

    async def download_images(self) -> List[str]:
        img_urls = await self.search_unsplash_images()

        if not img_urls:
            logger.warning("No images found.")
            return []

        tasks = [self.fetch_and_save_image(url, idx) for idx, url in enumerate(img_urls)]
        results = await asyncio.gather(*tasks)
        return [path for path in results if path is not None]

    async def run(self) -> List[str]:
        logger.info(f"Searching for images related to: {self.config.title}")
        saved_images = await self.download_images()
        logger.info("Download and modification process completed.")
        return saved_images

async def main(config: ImageConfig):
    downloader = UnsplashImageDownloader(config)
    
    try:
        saved_images = await downloader.run()
        if saved_images:
            logger.info(f"Successfully generated {len(saved_images)} images:")
            for img_path in saved_images:
                logger.info(f" - {img_path}")
        else:
            logger.warning("No images were successfully generated.")
    except aiohttp.ClientError as e:
        logger.error(f"Error connecting to Unsplash API: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download and modify images from Unsplash based on a given topic")
    parser.add_argument("title", help="The topic to search images for")
    parser.add_argument("subtitle", help="The subtitle to add to the images")
    parser.add_argument("--quality", type=int, default=90, help="PNG compression quality (1-100)")
    parser.add_argument("--per_page", type=int, default=3, help="Number of images to download")
    args = parser.parse_args()

    config = ImageConfig(args.title, args.subtitle, args.quality, args.per_page)
    
    # Configure DNS resolution
    socket.setdefaulttimeout(10)  # Set a timeout for DNS queries
    
    asyncio.run(main(config))
