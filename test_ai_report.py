"""
Teste do relatório semanal com IA
Execute este script para testar a nova funcionalidade.
"""

import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.services.weekly_report_service import WeeklyReportService
from src.services.database_service import DatabaseService
from src.models.review import Review
from src.config.settings import settings


def test_weekly_report():
    """Testa a geração do relatório semanal."""
    print("🧪 TESTE DO RELATÓRIO SEMANAL COM IA")
    print("=" * 50)
    
    # Inicializa serviços
    db_service = DatabaseService()
    report_service = WeeklyReportService()
    
    # Cria algumas avaliações de teste se não existirem
    print("📊 Verificando dados de teste...")
    reviews_result = db_service.get_all_reviews()
    
    if not reviews_result.success or len(reviews_result.data) < 2:
        print("📝 Criando avaliações de teste...")
        
        # Cria algumas avaliações de exemplo
        test_reviews = [
            Review(8, 7, 9, 8, "Dia produtivo", "Não treinei"),
            Review(7, 8, 7, 6, "Bom treino", "Estudos atrasados"),
            Review(9, 6, 8, 7, "Projeto finalizado", "Pouco exercício"),
            Review(6, 9, 6, 8, "Excelente treino", "Trabalho pesado"),
            Review(8, 7, 9, 8, "Dia equilibrado", "Nenhum ponto negativo")
        ]
        
        for review in test_reviews:
            result = db_service.insert_review(review)
            if result.success:
                print(f"✅ Avaliação criada: Média {review.get_average_score():.1f}")
            else:
                print(f"❌ Erro: {result.get_first_error()}")
    
    # Gera o relatório
    print("\n🤖 Gerando relatório semanal com IA...")
    result = report_service.generate_weekly_report()
    
    if result.success:
        print("✅ Relatório gerado com sucesso!")
        print("\n" + "="*60)
        print("📊 RELATÓRIO GERADO:")
        print("="*60)
        print(result.data['report'])
        print("="*60)
        
        # Mostra dados da análise
        analysis = result.data['analysis']
        print(f"\n🎯 Nível de Performance: {analysis['performance_level']}")
        print(f"📈 Área mais forte: {analysis['patterns']['strongest_area']}")
        print(f"📉 Área para melhorar: {analysis['patterns']['weakest_area']}")
        print(f"✨ Consistência: {analysis['patterns']['consistency_score']:.1f}/10")
        
    else:
        print(f"❌ Erro ao gerar relatório: {result.get_first_error()}")


def test_ai_analysis():
    """Testa apenas a análise de IA."""
    print("\n🧠 TESTE DA ANÁLISE DE IA")
    print("=" * 30)
    
    from src.services.ai_analysis_service import AIAnalysisService
    
    # Dados de exemplo
    weekly_data = {
        'avg_work': 7.5,
        'avg_training': 6.8,
        'avg_studies': 8.2,
        'avg_mind': 7.0,
        'total_reviews': 5,
        'overall_average': 7.375
    }
    
    # Reviews de exemplo
    reviews = [
        Review(8, 7, 9, 8, "Dia produtivo", "Não treinei"),
        Review(7, 8, 7, 6, "Bom treino", "Estudos atrasados"),
        Review(9, 6, 8, 7, "Projeto finalizado", "Pouco exercício")
    ]
    
    ai_service = AIAnalysisService()
    result = ai_service.analyze_weekly_data(weekly_data, reviews)
    
    if result.success:
        analysis = result.data
        print("✅ Análise de IA concluída!")
        print(f"🎯 Performance: {analysis['performance_level']}")
        print(f"💬 Mensagem: {analysis['motivational_message']}")
        print(f"📊 Insights: {len(analysis['insights'])} encontrados")
        print(f"🎯 Recomendações: {len(analysis['recommendations'])} geradas")
    else:
        print(f"❌ Erro na análise: {result.get_first_error()}")


if __name__ == "__main__":
    print(f"🎯 {settings.APP_NAME} v{settings.APP_VERSION}")
    print("Testando funcionalidades de IA...")
    
    # Testa análise de IA
    test_ai_analysis()
    
    # Testa relatório completo
    test_weekly_report()
    
    print("\n🎉 Testes concluídos!")
