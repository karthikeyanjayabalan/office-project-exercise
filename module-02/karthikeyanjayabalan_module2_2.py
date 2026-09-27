"""
module02-exercise02
====================
make python function code to encrypt a string. Make your own encryption method and explain it.
"""

def encrypt_string(input_string):
    # Simple encryption method: Shift each character by 3 positions in the ASCII table
    encrypted_string = ""
    
    for char in input_string:
        encrypted_string += chr(ord(char) + 3)
    
    return encrypted_string 

# --- Test Cases ---
encrypt_result = encrypt_string("Global Aerospace Logistics")
print("Encrypted String:", encrypt_result)  # Example usage with a string