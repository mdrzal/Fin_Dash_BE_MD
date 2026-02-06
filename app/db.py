import sqlite3
from pathlib import Path

_db_connection = None

def get_db_connection():
    global _db_connection
    if _db_connection is None:
        db_file = Path(__file__).parent / 'database.db'
        _db_connection = sqlite3.connect(str(db_file), check_same_thread=False)
    return _db_connection
