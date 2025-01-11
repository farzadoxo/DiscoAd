import sqlite3

class DataBase:
    """This class connect to Users Database"""

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()



