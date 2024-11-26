import sqlite3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def setup_database(setup="none"):
    if setup == "test":
        connection = sqlite3.connect("testdatabase.db")
    elif setup == "none":
        connection = sqlite3.connect("database.db")
    else:
        raise Exception("wrong setup argument")
    cursor = connection.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")
    with open('database/schema.sql', 'r') as schema:
        createSchema = schema.read()
    cursor.executescript(createSchema)
    with open('database/boilerplate.sql', 'r') as boilerplate:
        populateDatabase = boilerplate.read()
    cursor.executescript(populateDatabase)
    connection.commit()
    connection.close()
    
setup_database()