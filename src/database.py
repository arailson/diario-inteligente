import sqlite3

def connect_bank():
    conn = sqlite3.connect('data/reviews.db')
    return conn

def create_table():
    conn = connect_bank()
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            work INTEGER,
            training INTEGER,
            studies INTEGER,
            mind INTEGER,
            positive_points TEXT,
            negative_points TEXT
        )
    ''')
    
    conn.commit()
    conn.close()


def insert_data(work, training, studies, mind, positive_points, negative_points):
    conn = connect_bank()
    c = conn.cursor()
    
    c.execute('''
        INSERT INTO reviews (work, training, studies, mind, positive_points, negative_points)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (work, training, studies, mind, positive_points, negative_points))
    
    conn.commit()
    conn.close()
    
def consult_data():
    conn = connect_bank()
    c = conn.cursor()
    
    c.execute('SELECT * FROM reviews')
    results = c.fetchall()
    
    conn.close()
    return results