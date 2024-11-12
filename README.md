# Projet Enigma

## Description
Ce projet est une émulation de la machine Enigma en Python. Il inclut des fonctionnalités de chiffrement et de déchiffrement avec une configuration de rotors et un réflecteur personnalisables. L’interface est disponible en ligne de commande et avec une interface graphique.


## Fonctionnalités
- Chiffrement et déchiffrement de messages.
- Interface en ligne de commande et interface graphique.
- Configuration des rotors et du réflecteur via un fichier JSON.
- Possibilité de sauvegarder et de charger des configurations personnalisées.
- Mode verbose pour afficher les étapes de chiffrement/déchiffrement.
- Tests unitaires pour vérifier la validité du chiffrement et déchiffrement.


## Prérequis
- Python 3.x
- Tkinter (installé par défaut avec Python)


## Installation
1. Clonez le dépôt :
   ```bash
   git clone https://github.com/votre-depot/Projet_Enigma.git
2. Assurez-vous que toutes les dépendances sont installées si nécessaire.


## Utilisation
### Interface en ligne de commande
1. Exécutez le fichier cli_interface.py :
   ```bash
   python cli_interface.py
   ```
2. Choisissez si vous souhaitez charger la configuration par défaut ou une configuration personnalisée.
3. Entrez la clé initiale (ex: "ABC") pour définir la position de départ des rotors.
4. Sélectionnez le mode Chiffrer ou Déchiffrer.
5. Traitement d’un message : Entrez un message à chiffrer ou déchiffrer.
6. Traitement d’un fichier : Choisissez l’option F pour sélectionner un fichier texte à chiffrer ou déchiffrer. Le fichier sera traité et sauvegardé avec un suffixe _encrypted.txt ou _decrypted.txt.
7. Sauvegarde de configuration : Choisissez l'option S pour sauvegarder la configuration actuelle dans config/custom_config.json.


### Interface graphique
1. Exécutez le fichier gui_interface.py :
   ```bash
   python gui_interface.py
   ```
2. Entrez la clé initiale (ex: "ABC") pour définir la position de départ des rotors.
3. Choisissez les rotors et le réflecteur dans les menus déroulants.
4. Sélectionnez le mode Chiffrer ou Déchiffrer.
5. Traitement d’un message : Entrez un message dans le champ "Message à traiter" et cliquez sur Traiter.
6. Traitement d’un fichier : Cliquez sur Traiter un Fichier, sélectionnez un fichier texte, et le fichier sera traité et sauvegardé avec un suffixe _encrypted.txt ou _decrypted.txt.
7. Sauvegarde de configuration : Cliquez sur Sauvegarder Configuration pour sauvegarder la configuration actuelle dans config/custom_config.json.

## Tests unitaires
Lancez les tests unitaires pour vérifier que tout fonctionne correctement :
   ```bash
   python -m unittest discover -s tests
   ```


## Structure du projet
   ```bash
   Projet_Enigma/
   ├── config/
   │   └── config_manager.py
   │   └── custom_config.json 
   │   └── default_config.json # Fichier de configuration par défaut pour les rotors et le réflecteur
   ├── tests/
   │   ├── test_enigma.py      # Tests unitaires pour la machine Enigma
   │    └── test_rotor.py       # Tests unitaires pour le rotor
   ├── cli_interface.py        # Interface en ligne de commande
   ├── enigma_image.png
   ├── enigma_verbose.log
   ├── enigma.py               # Fichier principal de la machine Enigma
   ├── gui_interface.py        # Interface graphique
   ├── reflector.py            # Gestion du réflecteur
   ├── rotor.py                # Gestion des rotors
   └── README.md               # Documentation

   ```


## Auteur
Ce projet a été développé comme une simulation de la machine Enigma avec une personnalisation avancée et des tests unitaires.


## Exécution finale
1. Lance l'interface en ligne de commande :
   ```bash
   python cli_interface.py

   OU
   
2. Lance l'interface graphique :
   ```bash
   python gui_interface.py