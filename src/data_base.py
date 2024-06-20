import sqlite3
import os


def create_database(db_path):
    
    if not(os.path.exists(db_path)):
        # Connect to the database (it will be created if it doesn't exist)
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        # Create a table for ticker details with ticker as the primary key
        c.execute('''CREATE TABLE IF NOT EXISTS ticker_info (
                        ticker TEXT PRIMARY KEY,
                        ticker_type TEXT NOT NULL,
                        hashtags TEXT,
                        cashtag TEXT
                    )''')

        # Commit the changes and close the connection
        conn.commit()
        conn.close()
    else:
        print("Data base already Exist")
    

def insert_or_update_ticker(db_path,ticker, ticker_type, hashtags, cashtag):
    
    create_database(db_path)
    # Connect to the database
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Insert or update the ticker details
    c.execute('''INSERT OR REPLACE INTO ticker_info (ticker, ticker_type, hashtags, cashtag)
                VALUES (?, ?, ?, ?)''', (ticker, ticker_type, hashtags, cashtag))
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    
    
def fetch_all_tickers(db_path):
    
    if (os.path.exists(db_path)):
        # Connect to the database
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        # Fetch all records from the ticker_info table
        c.execute('SELECT * FROM ticker_info')
        rows = c.fetchall()
        
        # Close the connection
        conn.close()
        
        # Return the fetched rows
        return rows
    
    else:
        print("Data Base Don't Exist")


def fetch_ticker_by_name(ticker_name,db_path):
    
    if (os.path.exists(db_path)):
        # Connect to the database
        

        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        # Fetch the record with the specified ticker name
        c.execute('SELECT * FROM ticker_info WHERE ticker = ?', (ticker_name,))
        row = c.fetchone()
        
        # Close the connection
        conn.close()
        
        # Return the fetched row
        return row
    
    else:
        print("Data Base Don't Exist")
        return False


# databases/ticker_info.db


