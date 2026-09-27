"""
module01-exercise04
====================
make python function to return today date in this format (ss:mm:hh , day/month/year)
make python function to use current time (min) to find 2 * (current min) number of Fibonacci sequence. Display all sequence
"""

def get_current_time():
    from datetime import datetime
    now = datetime.now()
    return now.strftime("%I:%M:%S , %d/%m/%Y") # %I - 12 hrs format; %H - 24 hrs format

def fibonacci_sequence(n):
    sequence = []
    a, b = 0, 1
    for _ in range(n):
        sequence.append(a)
        a, b = b, a + b
    return sequence

# --- Test Cases ---
print(get_current_time())
# print(fibonacci_sequence(2 * 2))  # Example usage with a fixed number for demonstration
print(fibonacci_sequence(2 * int(get_current_time().split(':')[1])))
