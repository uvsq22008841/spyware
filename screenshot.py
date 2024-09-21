from PIL import ImageGrab
from datetime import datetime
import os

def screenshot(folder):
    """fait une capture d'ecran et la place dans le dossier specifie"""
    try:
        image = ImageGrab.grab()  # Capture l'écran
        date = datetime.now().strftime("%d_%m_%Y__%H-%M-%S")
        screenshot_information = f"screenshot_{date}.png"
        path = os.path.join(folder, screenshot_information)  # Définit le chemin du fichier

        #enregistre l'image dans le dossier
        image.save(path)
        print(f"capture d'écran enregistree dans: {path}")

    except Exception as e:
        print(f"erreur lors de la capture d'ecran:{e}")

def main():
    #recupere le chemin à partir d'une variable d'environnement
    folder = os.getenv('FOLDER_PATH')
    screenshot(folder)
    

if __name__ == "__main__":
    main()
