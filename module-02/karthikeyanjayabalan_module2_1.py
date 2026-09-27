"""
module02-exercise01
====================
make python function to show if a number is even or odd.
"""

def check_even_or_odd(number):
    if number % 2 == 0:
        return "Even"
    else:
        return "Odd"

# --- Test Cases ---
print("Result 1:", check_even_or_odd(5))   # Odd
print("Result 2:", check_even_or_odd(10))  # Even
