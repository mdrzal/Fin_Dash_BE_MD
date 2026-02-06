import csv
import sqlite3
from pathlib import Path
from app.services.logging_service import LoggingService
logger = LoggingService.get_logger(__name__)


def create_db(db_path: str):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS stock_symbols (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            sector TEXT,
            industry TEXT
        )
    ''')
    conn.commit()
    conn.close()
  
def insert_symbols_from_csv(db_path: str, csv_path: str):
    import yfinance as yf
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            symbol = row.get('Symbol')
            name = row.get('Security')
            sector = row.get('GICS Sector')
            industry = row.get('GICS Sub-Industry')
            if symbol and name:
                c.execute('INSERT OR IGNORE INTO stock_symbols (symbol, name, sector, industry) VALUES (?, ?, ?, ?)', (symbol, name, sector, industry))
    conn.commit()
    conn.close()

def initiate_db():
    db_file = Path(__file__).parent.parent / 'database.db'
    if not db_file.exists():
        create_db(str(db_file))
        csv_path = Path(__file__).parent / 'stocks.csv'
        insert_symbols_from_csv(str(db_file), str(csv_path))
        logger.info(f"Database created at {db_file} with symbols from CSV.")
    else:
        logger.info(f"Database already exists. No action taken.")