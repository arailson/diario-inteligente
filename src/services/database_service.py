"""
Serviço para operações de banco de dados.
Centraliza todas as operações relacionadas ao banco de dados.
"""

import sqlite3
import os
from typing import List, Optional
from ..models.review import Review
from ..models.result import Result
from ..config.settings import settings


class DatabaseService:
    """Classe para gerenciar operações de banco de dados."""
    
    def __init__(self):
        """Inicializa o serviço de banco de dados."""
        self.db_path = settings.DATABASE_PATH
        self._ensure_database_directory()
    
    def _ensure_database_directory(self):
        """Garante que o diretório do banco de dados existe."""
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
    
    def _get_connection(self) -> Result:
        """Estabelece conexão com o banco de dados."""
        try:
            conn = sqlite3.connect(self.db_path)
            return Result.success_result(conn)
        except Exception as e:
            return Result.error_result(f"Erro ao conectar com o banco: {str(e)}")
    
    def create_tables(self) -> Result:
        """Cria as tabelas necessárias no banco de dados."""
        try:
            conn_result = self._get_connection()
            if not conn_result.success:
                return conn_result
            
            conn = conn_result.data
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    work INTEGER NOT NULL CHECK (work >= 0 AND work <= 10),
                    training INTEGER NOT NULL CHECK (training >= 0 AND training <= 10),
                    studies INTEGER NOT NULL CHECK (studies >= 0 AND studies <= 10),
                    mind INTEGER NOT NULL CHECK (mind >= 0 AND mind <= 10),
                    positive_points TEXT NOT NULL,
                    negative_points TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            
            return Result.success_result("Tabelas criadas com sucesso!")
            
        except Exception as e:
            return Result.error_result(f"Erro ao criar tabelas: {str(e)}")
    
    def insert_review(self, review: Review) -> Result:
        """Insere uma nova avaliação no banco de dados."""
        try:
            conn_result = self._get_connection()
            if not conn_result.success:
                return conn_result
            
            conn = conn_result.data
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO reviews (work, training, studies, mind, positive_points, negative_points)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                review.work,
                review.training,
                review.studies,
                review.mind,
                review.positive_points,
                review.negative_points
            ))
            
            review.id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return Result.success_result(review)
            
        except Exception as e:
            return Result.error_result(f"Erro ao inserir avaliação: {str(e)}")
    
    def get_all_reviews(self) -> Result:
        """Retorna todas as avaliações do banco de dados."""
        try:
            conn_result = self._get_connection()
            if not conn_result.success:
                return conn_result
            
            conn = conn_result.data
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM reviews ORDER BY created_at DESC')
            rows = cursor.fetchall()
            
            reviews = []
            for row in rows:
                review_data = {
                    'id': row[0],
                    'work': row[1],
                    'training': row[2],
                    'studies': row[3],
                    'mind': row[4],
                    'positive_points': row[5],
                    'negative_points': row[6]
                }
                reviews.append(Review.from_dict(review_data))
            
            conn.close()
            return Result.success_result(reviews)
            
        except Exception as e:
            return Result.error_result(f"Erro ao buscar avaliações: {str(e)}")
    
    def get_reviews_by_date_range(self, start_date: str, end_date: str) -> Result:
        """Retorna avaliações dentro de um período específico."""
        try:
            conn_result = self._get_connection()
            if not conn_result.success:
                return conn_result
            
            conn = conn_result.data
            cursor = conn.cursor()
            
            # Verifica se a coluna created_at existe
            cursor.execute("PRAGMA table_info(reviews)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'created_at' in columns:
                # Se a coluna created_at existe, usa ela
                cursor.execute('''
                    SELECT * FROM reviews 
                    WHERE DATE(created_at) BETWEEN ? AND ?
                    ORDER BY created_at DESC
                ''', (start_date, end_date))
            else:
                # Se não existe, retorna todas as avaliações
                cursor.execute('SELECT * FROM reviews ORDER BY id DESC')
            
            rows = cursor.fetchall()
            
            reviews = []
            for row in rows:
                review_data = {
                    'id': row[0],
                    'work': row[1],
                    'training': row[2],
                    'studies': row[3],
                    'mind': row[4],
                    'positive_points': row[5],
                    'negative_points': row[6]
                }
                reviews.append(Review.from_dict(review_data))
            
            conn.close()
            return Result.success_result(reviews)
            
        except Exception as e:
            return Result.error_result(f"Erro ao buscar avaliações por período: {str(e)}")
    
    def get_weekly_average(self) -> Result:
        """Calcula a média semanal das avaliações."""
        try:
            conn_result = self._get_connection()
            if not conn_result.success:
                return conn_result
            
            conn = conn_result.data
            cursor = conn.cursor()
            
            # Primeiro, vamos verificar se a coluna created_at existe
            cursor.execute("PRAGMA table_info(reviews)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'created_at' in columns:
                # Se a coluna created_at existe, usa ela
                cursor.execute('''
                    SELECT 
                        AVG(work) as avg_work,
                        AVG(training) as avg_training,
                        AVG(studies) as avg_studies,
                        AVG(mind) as avg_mind,
                        COUNT(*) as total_reviews
                    FROM reviews 
                    WHERE created_at >= datetime('now', '-7 days')
                ''')
            else:
                # Se não existe, calcula a média de todas as avaliações
                cursor.execute('''
                    SELECT 
                        AVG(work) as avg_work,
                        AVG(training) as avg_training,
                        AVG(studies) as avg_studies,
                        AVG(mind) as avg_mind,
                        COUNT(*) as total_reviews
                    FROM reviews
                ''')
            
            result = cursor.fetchone()
            conn.close()
            
            if result and result[4] > 0:  # Se há avaliações
                weekly_data = {
                    'avg_work': round(result[0], 2),
                    'avg_training': round(result[1], 2),
                    'avg_studies': round(result[2], 2),
                    'avg_mind': round(result[3], 2),
                    'total_reviews': result[4],
                    'overall_average': round((result[0] + result[1] + result[2] + result[3]) / 4, 2)
                }
                return Result.success_result(weekly_data)
            else:
                return Result.error_result("Nenhuma avaliação encontrada.")
                
        except Exception as e:
            return Result.error_result(f"Erro ao calcular média semanal: {str(e)}")
