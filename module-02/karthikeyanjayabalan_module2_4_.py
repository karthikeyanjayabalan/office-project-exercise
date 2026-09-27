"""
module02-exercise04
====================
make python function to store a class type containing ( name , number , location , job title ) 
for 5 random people in Json file using json format. Create class and json file.
"""

def store_people_in_json(people_list, filename="module-02\\karthikeyanjayabalan_module02_exercise04_people.json"):
    import json

    try:
        with open(filename, "w") as file:
            json.dump(people_list, file, indent=4)
        print(f"People data has been stored in '{filename}' successfully.")
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")

# --- Test Cases ---
people_data = [
    {"name": "Alpha", "number": 1234567801, "location": "Abu Dhabi", "job_title": "Engineer"},
    {"name": "Bravo", "number": 1234567802, "location": "Dubai", "job_title": "Designer"},
    {"name": "Charlie", "number": 1234567803, "location": "Al Ain", "job_title": "Manager"},
    {"name": "Denver", "number": 1234567804, "location": "Fujairah", "job_title": "Developer"},
    {"name": "Echo", "number": 1234567805, "location": "Ras Al Khaimah", "job_title": "Analyst"}
]

store_people_in_json(people_data)