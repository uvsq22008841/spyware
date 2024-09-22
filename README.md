# Keylogger avec Capture d'Écran et Fonctionnalité d'Envoi par Email

## Aperçu

Ce projet implémente un keylogger qui capture les frappes au clavier et prend des captures d'écran à intervalles réguliers. Les données collectées sont cryptées et envoyées par email. Le script est conçu pour fonctionner sous Windows et inclut une fonctionnalité de démarrage automatique au lancement du système.

## Fonctionnalités

- Capture les frappes au clavier et les stocke dans un fichier journal.
- Prend des captures d'écran à intervalles réguliers.
- Crypte les images et les fichiers journaux à l'aide du chiffrement AES.
- Envoie les données collectées par email via Gmail.
- S'exécute au démarrage du système.

## Prérequis

- Python 3.x
- Bibliothèques requises :
  - `cv2` (OpenCV)
  - `pynput`
  - `Pillow`
  - `yagmail`
  - `cryptography`
  
Vous pouvez installer les bibliothèques requises avec pip :

```bash
pip install opencv-python pynput Pillow yagmail cryptography
