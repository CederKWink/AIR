import json
import os


class DBModel:
    def __init__(self, db_file="wood_database.json"):
        self.db_file = db_file
        self.data = {}  # In-memory storage as a dictionary
        self._initialize_db()

    def _initialize_db(self):
        """Read the database file into memory if it exists; otherwise, create it."""
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r') as f:
                self.data = {entry['ID']: entry for entry in json.load(f)}
        else:
            with open(self.db_file, 'w') as f:
                json.dump([], f)  # Create an empty file

    def insert(self, entry):
        """Insert a new entry into the in-memory database."""
        required_keys = {"ID", "length", "Width", "Height", "Destination"}
        if not required_keys.issubset(entry.keys()):
            raise ValueError(f"Entry must contain the keys: {required_keys}")

        if entry["ID"] in self.data:
            raise ValueError(f"Entry with ID {entry['ID']} already exists.")

        self.data[entry["ID"]] = entry
        print(f"Entry with ID {entry['ID']} added successfully.")

    def get_all(self):
        """Retrieve all entries from the in-memory database."""
        return list(self.data.values())

    def get_by_id(self, entry_id):
        """Retrieve a single entry by its ID."""
        return self.data.get(entry_id, None)

    def delete(self, entry_id):
        """Delete an entry by its ID."""
        if entry_id in self.data:
            del self.data[entry_id]
            print(f"Entry with ID {entry_id} deleted successfully.")
        else:
            print(f"No entry found with ID {entry_id}.")

    def _write_db(self):
        """Write the in-memory database to the file."""
        with open(self.db_file, 'w') as f:
            json.dump(list(self.data.values()), f, indent=4)

    def __del__(self):
        """Write the database to disk when the object is destroyed."""
        self._write_db()
        print(f"Database written to {self.db_file} on destruction.")