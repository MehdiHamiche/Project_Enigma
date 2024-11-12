from enigma import MachineEnigma
from rotor import Rotor
from reflector import Reflector
from config.config_manager import save_configuration, load_configuration

def encrypt_message_no_reset(machine, message, verbose=False):
    """
    Encrypts a message without resetting rotor positions.
    :param machine: Instance of the Enigma machine.
    :param message: Message to be encrypted.
    :param verbose: If True, shows verbose encryption steps.
    """
    encrypted_message = machine.encrypt(message, verbose=verbose)
    print(f"Encrypted message: {encrypted_message}")
    return encrypted_message

def main():
    # Choix de la configuration à charger
    config_choice = input("Voulez-vous charger la configuration par défaut (D) ou une configuration personnalisée (P) ? (D/P) : ").strip().upper()
    if config_choice == "P":
        config = load_configuration("config/custom_config.json")
    else:
        config = load_configuration("config/default_config.json")

    # Initialisation des rotors et du réflecteur avec la configuration chargée
    try:
        rotor1 = Rotor(config['rotors']['I']['wiring'], config['rotors']['I']['notch'])
        rotor2 = Rotor(config['rotors']['II']['wiring'], config['rotors']['II']['notch'])
        rotor3 = Rotor(config['rotors']['III']['wiring'], config['rotors']['III']['notch'])

        # Accessing the reflector properly
        reflector_key = 'B'  # You can change this to 'C' if needed
        reflector_wiring = config['reflectors'][reflector_key]  # Access the reflector wiring
        reflector = Reflector(reflector_wiring)

        machine = MachineEnigma([rotor1, rotor2, rotor3], reflector)

        # Demande de la clé de départ
        key = input("Entrez la clé initiale (ex: ABC) : ").upper()

        # Définir la position initiale des rotors
        machine.set_rotor_positions(key)

        # Mode verbose pour affichage étape par étape
        verbose = input("Souhaitez-vous activer le mode verbose ? (O/N) : ").strip().upper() == "O"

        # Demande de l'opération : traitement d'un message ou d'un fichier
        operation_type = input("Voulez-vous traiter un (M)essage ou un (F)ichier ? (M/F) : ").strip().upper()
    
        if operation_type == 'M':
            # Traitement d'un message simple
            operation = input("Voulez-vous (C)hiprer, (D)échiffrer ou (S)auvegarder la configuration ? (C/D/S) : ").strip().upper()
            if operation == 'C':
                message = input("Entrez le message à chiffrer : ").upper()
                # First encryption
                print("First Encryption:")
                first_encryption = encrypt_message_no_reset(machine, message, verbose=verbose)
                # Second encryption without resetting rotors
                print("\nSecond Encryption (without resetting rotors):")
                second_encryption = encrypt_message_no_reset(machine, message, verbose=verbose)    
                print(f"\nInput: {message}")
                print(f"Message chiffré : {first_encryption}")
            elif operation == 'D':
                message = input("Entrez le message à déchiffrer : ").upper()
                decrypted_message = machine.decrypt(message, verbose=verbose)
                print(f"Message déchiffré : {decrypted_message}")
            elif operation == 'S':
                # Sauvegarder la configuration actuelle
                save_configuration([rotor1, rotor2, rotor3], reflector, "config/custom_config.json")
                print("Configuration sauvegardée dans config/custom_config.json")
            else:
                print("Opération non reconnue.")

        elif operation_type == 'F':
            # Traitement d'un fichier
            filename = input("Entrez le chemin du fichier texte à traiter : ")
            operation = input("Voulez-vous (C)hiprer ou (D)échiffrer le fichier ? (C/D) : ").strip().upper()
        
            if operation in ['C', 'D']:
                encrypt_message_no_reset(machine, filename, operation, verbose=verbose)
            else:
                print("Opération non reconnue.")

    except KeyError as e:
        print(f"Erreur de configuration : clé manquante {e}")
    except TypeError as e:
        print(f"Erreur de type : {e}")

if __name__ == "__main__":
    main()