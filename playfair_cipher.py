import re

def prepare_key(key: str) -> str:
    """Prepare the key by removing duplicates and filling the alphabet."""
    key = re.sub(r'[^a-zA-Z]', '', key).upper()
    key = key.replace('J', 'I')  # I and J share the same position
    seen = set()
    cleaned_key = []
    
    for char in key:
        if char not in seen:
            cleaned_key.append(char)
            seen.add(char)
    
    # Add remaining letters (except J)
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    for char in alphabet:
        if char not in seen:
            cleaned_key.append(char)
    
    return ''.join(cleaned_key)

def create_matrix(key: str) -> list:
    """Create 5x5 Playfair matrix."""
    matrix = []
    key = prepare_key(key)
    for i in range(5):
        matrix.append(list(key[i*5 : (i+1)*5]))
    return matrix

def prepare_text(text: str) -> str:
    """Prepare the text for encryption/decryption."""
    text = re.sub(r'[^a-zA-Z]', '', text).upper()
    text = text.replace('J', 'I')
    
    # Split into digraphs and handle double letters
    i = 0
    result = []
    while i < len(text):
        if i == len(text) - 1:
            result.append(text[i] + 'X')
            break
        if text[i] == text[i+1]:
            result.append(text[i] + 'X')
            i += 1
        else:
            result.append(text[i] + text[i+1])
            i += 2
    return ' '.join(result)

def find_position(matrix: list, char: str) -> tuple:
    """Find the row and column of a character in the matrix."""
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == char:
                return (row, col)
    return (-1, -1)

def playfair_encrypt(plaintext: str, key: str) -> str:
    """Encrypt plaintext using Playfair cipher."""
    matrix = create_matrix(key)
    prepared_text = prepare_text(plaintext)
    ciphertext = []
    
    for digraph in prepared_text.split():
        a, b = digraph[0], digraph[1]
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)
        
        if row1 == row2:  # Same row
            ciphertext.append(matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5])
        elif col1 == col2:  # Same column
            ciphertext.append(matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2])
        else:  # Rectangle rule
            ciphertext.append(matrix[row1][col2] + matrix[row2][col1])
    
    return ''.join(ciphertext)

def playfair_decrypt(ciphertext: str, key: str) -> str:
    """Decrypt ciphertext using Playfair cipher."""
    matrix = create_matrix(key)
    prepared_text = prepare_text(ciphertext)
    plaintext = []
    
    for digraph in prepared_text.split():
        a, b = digraph[0], digraph[1]
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)
        
        if row1 == row2:  # Same row
            plaintext.append(matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5])
        elif col1 == col2:  # Same column
            plaintext.append(matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2])
        else:  # Rectangle rule
            plaintext.append(matrix[row1][col2] + matrix[row2][col1])
    
    return ''.join(plaintext)

if __name__ == "__main__":
    print("Playfair Cipher")
    action = input("Choose action (encrypt/decrypt): ").lower()
    text = input("Enter the text: ")
    key = input("Enter the key: ")
    
    if action == "encrypt":
        print("Encrypted text:", playfair_encrypt(text, key))
    elif action == "decrypt":
        print("Decrypted text:", playfair_decrypt(text, key))
    else:
        print("Invalid action!")