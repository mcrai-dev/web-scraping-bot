# Image Generator

![Screenshot du générateur d'images](exported_files/AI_4.png)

## Description

Ce projet est un générateur d'images qui, étant donné un titre ou un sujet, recherche une image pertinente sur Unsplash et la modifie en ajoutant un titre, un sous-titre et un code QR.

## Fonctionnalités

* Recherche d'images sur Unsplash en fonction d'un titre ou d'un sujet
* Modification des images en ajoutant un titre, un sous-titre et un code QR
* Génération d'images prêtes à l'emploi pour les présentations, les billets de blog, les réseaux sociaux, etc.

## Technologies utilisées

* Python
* API Unsplash
* Pillow (bibliothèque Python pour la manipulation d'images)
* qrcode (bibliothèque Python pour la génération de codes QR)

## Installation

1. Clonez ce dépôt :
   ```
   git clone https://github.com/mcrai-dev/web-scraping-bot.git
   cd web-scraping-bot
   ```

2. Installez les dépendances requises :
   ```
   pip install -r requirements.txt
   ```

3. Créez un compte sur [Unsplash](https://unsplash.com/developers) et obtenez une clé API

4. Créez un fichier `.env` à la racine du projet et ajoutez votre clé API :

```python
UNSPLASH_API_KEY = "votre-clé-api-ici"
```

## Utilisation

Exécutez le script `script.py` en passant le titre et le sous-titre comme arguments, par exemple :

```sh
python script.py "AI" "Technology for the futur" --quality 90 --per_page 5
```

Options :
- `--quality` : Qualité de l'image de sortie (0-100, par défaut : 85)
- `--per_page` : Nombre d'images à récupérer d'Unsplash (par défaut : 3)

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou à soumettre une pull request.

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.# web-scraping-bot
