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
```


## Instructions pour Exécuter le Script Python

Pour exécuter le script Python, suivez ces étapes :

1. **Assurez-vous que Python est installé** :
   - Vérifiez si Python est installé en ouvrant un terminal (ou l'invite de commande) et en tapant :
     ```bash
     python --version
     ```
   - Si Python n'est pas installé, téléchargez-le.

2. **Installez les bibliothèques requises** :
   - Ouvrez le terminal et installez les bibliothèques nécessaires avec la commande suivante :
     ```bash
     pip install opencv-python pynput Pillow yagmail cryptography
     ```

3. **Téléchargez le script** :
   - Téléchargez le fichier du script Python "final.py" et placez-le dans un répertoire de votre choix.

4. **Modifiez le script** :
   - Ouvrez le script dans un éditeur de texte et modifiez les informations nécessaires, comme vos identifiants Gmail et le chemin de la clé publique RSA.

5. **Exécutez le script** :
   - Dans le terminal, naviguez jusqu'au répertoire contenant le script. Par exemple :
     ```bash
     cd "C:\Users\votre_nom\Chemin\Vers\Le\Dossier"
     ```
   - Exécutez le script avec la commande :
     ```bash
     python final.py
     ```

6. **Vérifiez l'exécution** :
   - Le script devrait démarrer en arrière-plan. Vous pouvez vérifier que les captures d'écran et les journaux sont créés dans le dossier spécifié.

7. **Arrêt du script** :
   - Pour arrêter le script, vous pouvez simplement fermer la fenêtre du terminal ou utiliser `Ctrl + C`.


