from datacenter import DataBase


def makedatabase():
    DataBase.cursor.execute(
        """CREATE TABLE table1 (userid INTEGER ,
        balance INTEGER PRIMARY KEY NOT NULL ,
        count INTEGER ,
        warnings INTEGER)"""
    )

if __name__ == "__main__":
    makedatabase()
