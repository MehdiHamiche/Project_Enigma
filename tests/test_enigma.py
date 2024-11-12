import unittest
from enigma import MachineEnigma
from rotor import Rotor
from reflector import Reflector

class TestEnigmaMachine(unittest.TestCase):
    def setUp(self):
        rotor1 = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q")
        rotor2 = Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E")
        rotor3 = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V")
        reflector = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")
        self.machine = MachineEnigma([rotor1, rotor2, rotor3], reflector)

    def test_chiffrement_dechiffrement(self):
        message = "HELLO"
        
        # Chiffrement
        self.machine.set_rotor_positions("ABC")
        encrypted = self.machine.encrypt(message)

        # Déchiffrement
        self.machine.set_rotor_positions("ABC")
        decrypted = self.machine.decrypt(encrypted)

        # Vérifie que le message d'origine est retrouvé
        self.assertEqual(message, decrypted)

if __name__ == "__main__":
    unittest.main()
