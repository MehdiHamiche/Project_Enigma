import unittest
from enigma import MachineEnigma
from rotor import Rotor
from reflector import Reflector

class TestEnigmaMachine(unittest.TestCase):
    def setUp(self):
        # Configuration des rotors et du réflecteur pour les tests
        rotor1 = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q")
        rotor2 = Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E")
        rotor3 = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V")
        reflector = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")

        # Crée une instance de la machine avec les rotors et réflecteur configurés
        self.machine = MachineEnigma([rotor1, rotor2, rotor3], reflector)

    def test_chiffrement_dechiffrement(self):
        # Message d'origine
        message = "HELLO"
        
        # Chiffrement
        self.machine.set_rotor_positions("ABC")
        encrypted = self.machine.encrypt(message)

        # Déchiffrement
        self.machine.set_rotor_positions("ABC")  # Remettre les rotors à la position initiale
        decrypted = self.machine.decrypt(encrypted)

        # Vérification
        self.assertEqual(message, decrypted)

if __name__ == "__main__":
    unittest.main()
