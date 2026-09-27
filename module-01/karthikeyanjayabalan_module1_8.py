"""
module01-exercise08
====================
make python code to read the text file you made with people address (Q.6). 
Then return word count for each address. Append the word count into the same file.
"""

def append_word_count_to_address_file(filename="module-01\\karthikeyanjayabalan_module01_exercise06_saveaddress.txt"):
    try:
        with open(filename, "r") as file:
            lines = file.readlines()

        with open(filename, "a") as file:
            for line in lines:
                if line.strip() and not line.startswith("-"):
                    word_count = len(line.split())
                    file.write(f"Word Count: {word_count}\n")
            file.write("-" * 40 + "\n")  # Separator for entries

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# --- Test Cases ---
append_word_count_to_address_file()  # Example usage with the default filename