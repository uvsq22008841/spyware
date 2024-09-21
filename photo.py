import cv2, os
from datetime import datetime




def capture_image():
    """capture une photo en utilisant la camera du pc"""
    camera = cv2.VideoCapture(0)

    try:
        if not camera.isOpened():
            print("Erreur:camera inaccessible\n")
            return None
        #capture plusieurs images pour laisser la camera s'ajuster
        for _ in range(2):  
            success, image = camera.read()

        return image if success else None

    except Exception as e:
        print(f"erreur lors de la capture de l'image : {e}")
        return None

    finally:
         #libere la camera
        camera.release() 
       


def save_image(img, folder):
    """enregistre l'image dans le dossier specifie"""
    date = datetime.now().strftime("%d_%m_%Y__%H-%M-%S")

    #definit le nom du fichier 
    filename = f"photo_{date}.png"
    path = os.path.join(folder, filename)
    
    # enregistre l'image dans le fichier
    cv2.imwrite(path, img)

def main():

    folder = os.getenv('FOLDER_PATH')
    captured_img = capture_image()
    if captured_img is not None:
        save_image(captured_img, folder)

if __name__ == "__main__":
   
    main()

