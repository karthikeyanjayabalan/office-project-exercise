"""
module01-exercise07
====================
make python code to accept only string and display it (try. Except). 
If the pass value is not a string return NULL
"""

def check_and_display_string(value):
    try:
        # Check if the passed value is an instance of a string
        if not isinstance(value, str):
            raise TypeError("Value is not a string.")
        
        # If it is a string, display it
        print("Displayed String:", value)
        return value
        
    except TypeError:
        # If a non-string type raises the error, return None (NULL)
        return None

# --- Test Cases ---
print("Result 1:", check_and_display_string("Karthikeyan Jayabalan, GAL7535"))  # Valid string
print("Result 2:", check_and_display_string(7535))          # Integer (not a string)
print("Result 3:", check_and_display_string(["A", "B"]))     # List (not a string)