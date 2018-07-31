import sqlite3


class Connection:
    @staticmethod
    def init_DB():
        """Returns a connection after running DB init processes"""
        conn = sqlite3.connect('clip.db')
        conn.execute('''DROP TABLE IF EXISTS Clipboard''')  # For testing
        conn.execute('''CREATE TABLE Clipboard
                    (ID    INTEGER PRIMARY KEY AUTOINCREMENT   NOT NULL,
                    TEXT   TEXT                                NOT NULL);''')
        return conn

    @staticmethod
    def get_last_record(conn):
        """Gets the most recent Clipboard record stored in the DB"""
        cursor = conn.execute('''SELECT TEXT FROM Clipboard ORDER BY ID DESC LIMIT 1''')
        last_db_record = cursor.fetchone()
        return last_db_record

    @staticmethod
    def insert_new_record(conn, data):
        """Inserts a record into the Clipboard table then prints the data"""
        conn.execute('''INSERT INTO Clipboard (TEXT) 
                                    VALUES (?)''', (data,))
        conn.commit()
