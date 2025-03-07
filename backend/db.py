import csv
import sqlite3

def initialize_database():
    """Initialize the database and create necessary tables if they don't exist."""
    conn = sqlite3.connect("jarvis.db")
    cursor = conn.cursor()

    # Create system commands table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sys_command(
        id integer primary key, 
        name VARCHAR(100), 
        path VARCHAR(1000)
    )
    """)

    # Create web commands table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS web_command(
        id integer primary key, 
        name VARCHAR(100), 
        url VARCHAR(1000)
    )
    """)

    # Create contacts table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY, 
        name VARCHAR(200), 
        Phone VARCHAR(255), 
        email VARCHAR(255) NULL
    )
    """)

    conn.commit()
    conn.close()
    print("Database initialized successfully")

def import_contacts_from_csv(csv_file_path):
    """Import contacts from a CSV file into the database."""
    conn = sqlite3.connect("jarvis.db")
    cursor = conn.cursor()
    
    # Columns to import (name and phone)
    desired_columns_indices = [0, 20]
    
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                if len(row) > max(desired_columns_indices):
                    selected_data = [row[i] for i in desired_columns_indices]
                    cursor.execute(
                        'INSERT INTO contacts (id, name, Phone) VALUES (null, ?, ?);', 
                        tuple(selected_data)
                    )
        
        conn.commit()
        print("Contacts imported successfully")
    except Exception as e:
        print(f"Error importing contacts: {e}")
    finally:
        conn.close()

def add_system_command(name, path):
    """Add a system command to the database."""
    conn = sqlite3.connect("jarvis.db")
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO sys_command VALUES (null, ?, ?)",
            (name, path)
        )
        conn.commit()
        print(f"System command '{name}' added successfully")
    except Exception as e:
        print(f"Error adding system command: {e}")
    finally:
        conn.close()

def add_web_command(name, url):
    """Add a web command to the database."""
    conn = sqlite3.connect("jarvis.db")
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO web_command VALUES (null, ?, ?)",
            (name, url)
        )
        conn.commit()
        print(f"Web command '{name}' added successfully")
    except Exception as e:
        print(f"Error adding web command: {e}")
    finally:
        conn.close()

def add_contact(name, phone, email=None):
    """Add a contact to the database."""
    conn = sqlite3.connect("jarvis.db")
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO contacts VALUES (null, ?, ?, ?)",
            (name, phone, email)
        )
        conn.commit()
        print(f"Contact '{name}' added successfully")
    except Exception as e:
        print(f"Error adding contact: {e}")
    finally:
        conn.close()

# Initialize the database when this module is imported
if __name__ == "__main__":
    initialize_database()

