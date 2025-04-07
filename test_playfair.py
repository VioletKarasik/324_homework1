import unittest
from playfair_cipher import (
    prepare_key,
    create_matrix,
    prepare_text,
    playfair_encrypt,
    playfair_decrypt
)

class TestPlayfairCipher(unittest.TestCase):
    def test_prepare_key(self):
        self.assertEqual(prepare_key("playfair example"), "PLAYFIREXMBCDGHKNOQSTUVWZ")
        self.assertEqual(prepare_key("jazz"), "IAZBCDEFGHKLMNOPQRSTUVWXY")
    
    def test_create_matrix(self):
        key = "playfair example"
        expected = [
            ['P', 'L', 'A', 'Y', 'F'],
            ['I', 'R', 'E', 'X', 'M'],
            ['B', 'C', 'D', 'G', 'H'],
            ['K', 'N', 'O', 'Q', 'S'],
            ['T', 'U', 'V', 'W', 'Z']
        ]
        self.assertEqual(create_matrix(key), expected)
    
    def test_prepare_text(self):
        self.assertEqual(prepare_text("hello world"), "HE LX LO WO RL DX")  # 11 chars → adds X
        self.assertEqual(prepare_text("balloon"), "BA LX LO ON")  # 7 chars → adds X
        self.assertEqual(prepare_text("jazz"), "IA ZX ZX")  # even length, but double letters

    
    def test_encrypt_decrypt(self):
        key = "playfair example"
        plaintext = "hide the gold in the tree stump"
        encrypted = playfair_encrypt(plaintext, key)
        decrypted = playfair_decrypt(encrypted, key)
        
        # Remove X's added during preparation
        decrypted = decrypted.replace('X', '')
        self.assertEqual(decrypted, "HIDETHEGOLDINTHETREESTUMP")
    
    def test_known_encryption(self):
        key = "monarchy"
        plaintext = "instruments"
        encrypted = playfair_encrypt(plaintext, key)
        self.assertEqual(encrypted, "GATLMZCLRQXA")
        
        decrypted = playfair_decrypt(encrypted, key)
        decrypted = decrypted.replace('X', '')
        self.assertEqual(decrypted, "INSTRUMENTS")

if __name__ == "__main__":
    unittest.main()