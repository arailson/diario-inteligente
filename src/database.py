"""
Arquivo de migração - pode ser removido após confirmar que tudo funciona.
Este arquivo mantém compatibilidade com o código antigo.
"""

# Importa as novas classes para manter compatibilidade
from .models.result import Result
from .services.database_service import DatabaseService

# Cria instância global do serviço
_db_service = DatabaseService()

# Funções de compatibilidade (podem ser removidas depois)
def connect_bank():
    """Função de compatibilidade - use DatabaseService diretamente."""
    return _db_service._get_connection()

def create_table():
    """Função de compatibilidade - use DatabaseService diretamente."""
    return _db_service.create_tables()

def insert_data(work, training, studies, mind, positive_points, negative_points):
    """Função de compatibilidade - use DatabaseService diretamente."""
    from .models.review import Review
    
    try:
        review = Review(
            work=work,
            training=training,
            studies=studies,
            mind=mind,
            positive_points=positive_points,
            negative_points=negative_points
        )
        return _db_service.insert_review(review)
    except Exception as e:
        return Result.error_result(str(e))

def consult_data():
    """Função de compatibilidade - use DatabaseService diretamente."""
    return _db_service.get_all_reviews()