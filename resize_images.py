import os
import sys
import random
import datetime
import logging
from PIL import Image, ImageEnhance

# Détecter si le script tourne sous PyInstaller et récupérer le bon dossier
if getattr(sys, 'frozen', False):
    script_dir = os.path.dirname(sys.executable)  # Dossier où se trouve ResizeImages.exe
else:
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Dossier du script normal

# Définition des dossiers
input_folder = os.path.join(script_dir, "images_origines")
log_file = os.path.join(script_dir, "log.txt")

# Configuration du logging
logging.basicConfig(filename=log_file, level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

logging.info("Lancement du script ResizeImages")

def resize_images():
    try:
        logging.info("Début de la fonction resize_images()")

        # Vérifier si le dossier d'entrée existe
        if not os.path.exists(input_folder):
            logging.error(f"Le dossier {input_folder} n'existe pas.")
            return

        # Générer un dossier de sortie avec la date et l'heure
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_folder = os.path.join(script_dir, f"images_redimensionnees_{timestamp}")

        # Créer le dossier de sortie s'il n'existe pas
        os.makedirs(output_folder, exist_ok=True)
        logging.info(f"Dossier de sortie créé : {output_folder}")

        # Générer un facteur de zoom unique pour cette exécution
        zoom_factor = random.uniform(1.03, 1.05)
        logging.info(f"Facteur de zoom appliqué : {zoom_factor:.2f}")

        # Parcourir les fichiers du dossier
        for filename in os.listdir(input_folder):
            if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
                try:
                    file_path = os.path.join(input_folder, filename)
                    logging.info(f"Traitement de l'image : {filename}")

                    with Image.open(file_path) as img:
                        width, height = img.size
                        new_width = int(width / zoom_factor)
                        new_height = int(height / zoom_factor)

                        # Définir les coordonnées pour recadrer au centre
                        left = (width - new_width) // 2
                        top = (height - new_height) // 2
                        right = left + new_width
                        bottom = top + new_height

                        # Recadrer l'image
                        cropped_img = img.crop((left, top, right, bottom))

                        # Redimensionner pour conserver la taille d'origine
                        final_img = cropped_img.resize((width, height), Image.Resampling.LANCZOS)

                        # Ajuster légèrement la luminosité
                        brightness_factor = random.uniform(0.98, 1.02)  # Variation de ±2%
                        enhancer = ImageEnhance.Brightness(final_img)
                        final_img = enhancer.enhance(brightness_factor)
                        logging.info(f"Facteur de luminosité appliqué : {brightness_factor:.2f}")

                        # Sauvegarde
                        output_filename = f"zoomed_{timestamp}_{filename}"
                        output_path = os.path.join(output_folder, output_filename)
                        final_img.save(output_path)

                        logging.info(f"Image traitée et enregistrée : {output_path}")

                except Exception as e:
                    logging.error(f"Erreur avec {filename} : {str(e)}")

    except Exception as e:
        logging.critical(f"Erreur critique : {str(e)}")

if __name__ == "__main__":
    resize_images()
    logging.info("Fin du script")
