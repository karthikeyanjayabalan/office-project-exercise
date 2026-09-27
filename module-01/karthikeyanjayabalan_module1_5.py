"""
module01-exercise05
===================
make python function given a string of words and price for a letter. 
It will shift only letters by one (E.g. a -> b) and return (shifted string, word count, price of string) 
in dictionary format.
"""

def shift_string_and_calculate_price(input_string, price_per_letter):
    shifted_string = ""
    letter_count = 0
    
    for char in input_string:
        if char.isalpha():
            letter_count += 1
            if char == 'z':
                shifted_string += 'a'
            elif char == 'Z':
                shifted_string += 'A'
            else:
                shifted_string += chr(ord(char) + 1)
        else:
            shifted_string += char
    
    word_count = len(input_string.split())
    total_price = letter_count * price_per_letter
    
    return {
        "shifted_string": shifted_string,
        "word_count": word_count,
        "total_price": total_price
    }

# --- Test Cases ---
shifted_result = shift_string_and_calculate_price("Global Aerospace Logistics", 1)
print(shifted_result)  # Example usage with a string and price per letter   