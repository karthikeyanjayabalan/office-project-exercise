"""
module02-exercise03
====================
make python function for a given list of numbers. Find the unique list of numbers.
"""

def find_unique_numbers(input_list):
    unique_numbers = list(set(input_list))
    return unique_numbers

# --- Test Cases ---
unique_result = find_unique_numbers([1, 2, 2, 3, 4, 4, 5, 5, 6])
print("Unique Numbers:", unique_result)  # Example usage with a list of numbers
