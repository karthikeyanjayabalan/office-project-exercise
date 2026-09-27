"""
module01-exercise03
====================
make python function to print any type variable. It should return (variable content + data type).
"""

def print_variable_info(variable):
    variable_content = str(variable)
    variable_type = type(variable)
    return f"Variable Content: {variable_content}, Data Type: {variable_type}"

# --- Test Cases ---
print(print_variable_info(7535))  # Example usage with an integer
print(print_variable_info("Global Aerospace Logistics"))  # Example usage with a string
print(print_variable_info(["GAL", 7535, True, False]))  # Example usage with a list
print(print_variable_info({"key": "value"}))  # Example usage with a dictionary 