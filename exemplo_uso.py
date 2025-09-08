"""
Exemplo de uso do Diário Inteligente
Este arquivo mostra como usar as classes diretamente.
"""

from src.models.review import Review
from src.services.database_service import DatabaseService
from src.services.email_service import EmailService
from src.config.settings import settings


def exemplo_uso():
    """Exemplo de como usar o sistema programaticamente."""
    
    # Inicializa os serviços
    db_service = DatabaseService()
    email_service = EmailService()
    
    # Cria as tabelas
    print("Criando tabelas...")
    result = db_service.create_tables()
    if not result.success:
        print(f"Erro: {result.get_first_error()}")
        return
    
    # Cria uma avaliação
    print("Criando avaliação...")
    review = Review(
        work=8,
        training=7,
        studies=9,
        mind=8,
        positive_points="Dia produtivo, terminei um projeto importante",
        negative_points="Não consegui fazer exercícios"
    )
    
    # Salva no banco
    result = db_service.insert_review(review)
    if result.success:
        print("✅ Avaliação salva!")
        print(f"Média: {review.get_average_score():.1f}")
    else:
        print(f"❌ Erro: {result.get_first_error()}")
    
    # Busca todas as avaliações
    print("\nBuscando avaliações...")
    result = db_service.get_all_reviews()
    if result.success:
        reviews = result.data
        print(f"Encontradas {len(reviews)} avaliações")
        for review in reviews:
            print(f"- ID: {review.id}, Média: {review.get_average_score():.1f}")
    
    # Calcula média semanal
    print("\nCalculando média semanal...")
    result = db_service.get_weekly_average()
    if result.success:
        data = result.data
        print(f"Média geral: {data['overall_average']}")
    else:
        print(f"❌ Erro: {result.get_first_error()}")


if __name__ == "__main__":
    exemplo_uso()
