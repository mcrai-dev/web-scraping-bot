# Image Generator

![Screenshot du générateur d'images](exported_files/AI_4.png)

## Description

This project is an image generator that, given a title or topic, searches for a relevant image on Unsplash and modifies it by adding a title, a subtitle, and a QR code.

## Features

* Searches for images on Unsplash based on a title or topic
* Modifies images by adding a title, a subtitle, and a QR code
* Generates ready-to-use images for presentations, blog posts, social media, etc.

## Technology Used

* Python
* API Unsplash
* Pillow (Python library for image manipulation))
* qrcode (Python library for QR code generation)

## Installation

1. Clone this repository :
   ```
   git clone https://github.com/mcrai-dev/web-scraping-bot.git
   cd web-scraping-bot
   ```

2. Install the required dependencies :
   ```
   pip install -r requirements.txt
   ```

3. Create an account on [Unsplash](https://unsplash.com/developers) and obtain an API key

4. Create a `.env` file at the root of the project and add your API key :

```python
UNSPLASH_API_KEY = "votre-clé-api-ici"
```

## Usage

Run the `script.py` script by passing the title and subtitle as arguments, for example :

```sh
python script.py "AI" "Technology for the futur" --quality 90 --per_page 5
```

Options :
- `--quality` : Quality of the output image (0-100, default: 85)
- `--per_page` : Number of images to retrieve from Unsplash (default: 3)
  
## Contribution

Contributions are welcome! Feel free to open an issue or submit a pull request.


## Licence

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.# web-scraping-bot
