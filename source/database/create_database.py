from datacenter import DataBase


DataBase.cursor.execute(
    """CREATE TABLE table1 (userid INTEGER , balance INTEGER , count INTEGER , warnings INTEGER)"""
)

