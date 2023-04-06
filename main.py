from db import Database
from GUI import GUI

if __name__ == '__main__':
    db = Database("database.sqlite3")
    db.create_database()
    gui = GUI()
