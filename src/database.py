import sqlite3
from src.results import Results

def connect_bank():
    try:
        conn = sqlite3.connect('data/reviews.db')
        
        return Results(success=True, data=conn)
    
    except Exception as e:
        return Results(success=False, error_message=[str(e)])
        


def create_table():
    try:
        conn_result = connect_bank()
        if not conn_result.success:
            return conn_result
        
        conn = conn_result.data
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
        
        return Results(success=True, data=None)
    
    except Exception as e:
        return Results(success=False, error_message=[str(e)])
    
    finally:
        if 'conn' in locals() and conn:
            conn.close()
        


def insert_data(work, training, studies, mind, positive_points, negative_points):
    try:
        errors = []
        
         # Validação dos campos de nota (work, training, studies, mind)
        if not all(isinstance(i, (int, float)) for i in [work, training, studies, mind]):
            errors.append("Todos os campos de notas (work, training, studies, mind) devem ser números válidos.")
            
        for field, value in [("work", work), ("training", training), ("studies", studies), ("mind", mind)]:
            if value is None or value < 0 or value > 10:
                errors.append(f"O campo {field} deve estar entre 0 e 10 e não pode ser vazio.")
                
        if positive_points is None or not isinstance(positive_points, str) or not positive_points.strip():
            errors.append("O campo 'positive_points' deve ser uma string não vazia.")
    
        if negative_points is None or not isinstance(negative_points, str) or not negative_points.strip():
            errors.append("O campo 'negative_points' deve ser uma string não vazia.")
            
        if errors:
            return Results(success=False, error_message=errors)
        
        conn_result = connect_bank()
        if not conn_result.success:
            return conn_result
        
        conn = conn_result.data
        c = conn.cursor()
        
        c.execute('''
            INSERT INTO reviews (work, training, studies, mind, positive_points, negative_points)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (work, training, studies, mind, positive_points, negative_points))
        
        conn.commit()
        conn.close()
        
        return Results(success=True, data=None)
        
    except Exception as e:
        return Results(success=False, error_message=[str(e)])
    
    finally:
        if 'conn' in locals() and conn:
            conn.close()
        
        
    
def consult_data():
    try:
        conn_result = connect_bank()
        if not conn_result.success:
            return conn_result
        
        conn = conn_result.data
        c = conn.cursor()
        
        c.execute('SELECT * FROM reviews')
        results = c.fetchall()
        
        conn.close()
        return Results(success=True, data=results)
    
    except Exception as e:
        return Results(success=False, error_message=[str(e)])
    
    finally:
        if 'conn' in locals() and conn:
            conn.close()
        