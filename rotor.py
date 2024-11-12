class Rotor:
    def __init__(self, wiring, notch, position=0, ring_setting=0):
        """
        Initialise un rotor avec sa configuration de câblage, sa position et son réglage d'anneau.
        :param wiring: Chaîne représentant la substitution du rotor.
        :param notch: La position où le rotor déclenche le rotor suivant.
        :param position: La position initiale du rotor.
        :param ring_setting: Réglage de l'anneau du rotor.
        """
        self.wiring = wiring
        self.notch = ord(notch) - ord('A') if isinstance(notch, str) else notch
        self.position = position
        self.ring_setting = ring_setting

    def rotate(self):
        """
        Fait tourner le rotor d'une position.
        Renvoie True si le rotor atteint la position de la 'notch' (encoche).
        """
        self.position = (self.position + 1) % 26
        return self.position == self.notch    

    def encrypt_forward(self, char):
        """
        Chiffre la lettre dans le sens avant (de l'entrée au réflecteur).
        :param char: Lettre à chiffrer.
        :return: Lettre après chiffrement par le rotor.
        """
        index = (ord(char) - ord('A') + self.position - self.ring_setting) % 26
        encrypted_char = self.wiring[index]
        print(f"Encrypting Forward: {char} -> {encrypted_char} (index: {index})")  # Debugging line
        return encrypted_char  # Returning directly without additional adjustment
    
    def encrypt_backward(self, char):
        """
        Chiffre la lettre dans le sens arrière (du réflecteur vers l'entrée).
        :param char: Lettre à déchiffrer.
        :return: Lettre après transformation inverse par le rotor.
        """
        # Find the index of the character in wiring and adjust for ring and position
        index = (self.wiring.index(char) - self.position + self.ring_setting) % 26
        decrypted_char = chr(index + ord('A'))  # Adjusting the index calculation
        print(f"Decrypting Backward: {char} -> {decrypted_char} (index: {index})")  # Debugging line
        return decrypted_char

    def __str__(self):
        """
        Représentation textuelle pour le débogage.
        """
        return f"Rotor(wiring: {self.wiring}, position: {self.position}, ring_setting: {self.ring_setting})"