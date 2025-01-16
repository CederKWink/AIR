from db_model import DBModel

# Example usage
if __name__ == "__main__":
    db = DBModel()

    # Insert a new wood entry
    woods = [
        {
        "ID": 1,
        "length": 1189,
        "Width": 19,
        "Height": 49,
        "Destination": 1
        },
        {
        "ID": 2,
        "length": 1279,
        "Width": 13,
        "Height": 91,
        "Destination": 2
        },
        {
        "ID": 3,
        "length": 1699,
        "Width": 19,
        "Height": 119,
        "Destination": 3
        },
        {
        "ID": 4,
        "length": 1710,
        "Width": 25,
        "Height": 68,
        "Destination": 4
        },
        {
        "ID": 5,
        "length": 2138,
        "Width": 19,
        "Height": 118,
        "Destination": 5
        },
        {
        "ID": 6,
        "length": 2240,
        "Width": 19,
        "Height": 89,
        "Destination": 6
        }
    ]

    # try:
    #     for wood in woods:
    #         db.insert(wood)
    # except ValueError as e:
    #     print(e)

    # Retrieve and display all entries
    all_entries = db.get_all()
    print("Current database entries:")
    for entry in all_entries:
        print(entry)