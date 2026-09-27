"""
module01-exercise06
====================
make python function to make a class to save address of person (name, contact, address, phone number). 
The use will input the values. The address should be saved in .text file
"""

def save_address_to_file(name, contact, address, phone_number, filename="module-01\\karthikeyanjayabalan_module01_exercise06_saveaddress.txt"):
    with open(filename, "a") as file:
        file.write(f"Name: {name}\n")
        file.write(f"Contact: {contact}\n")
        file.write(f"Address: {address}\n")
        file.write(f"Phone Number: {phone_number}\n")
        file.write("-" * 40 + "\n")  # Separator for entries    

# --- Test Cases ---
save_address_to_file("Karthikeyan", "karthikeyan.j@gal.ae", "18, Khartoum Street, Muroor Road, Abu Dhabi", "056-236-8949")