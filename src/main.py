"""
Diário Inteligente - Aplicação Principal
Sistema para registrar e avaliar aspectos do dia a dia.
"""

from src.models.review import Review
from src.models.result import Result
from src.services.database_service import DatabaseService
from src.services.email_service import EmailService
from src.services.weekly_report_service import WeeklyReportService
from src.config.settings import settings


class DiarioInteligente:
    """Classe principal da aplicação."""
    
    def __init__(self):
        """Inicializa a aplicação."""
        self.db_service = DatabaseService()
        self.email_service = EmailService()
        self.report_service = WeeklyReportService()
    
    def initialize(self) -> Result:
        """Inicializa o banco de dados."""
        print("Inicializando Diário Inteligente...")
        settings.print_config()
        
        # Cria as tabelas necessárias
        result = self.db_service.create_tables()
        if result.success:
            print("✅ Banco de dados inicializado com sucesso!")
        else:
            print(f"❌ Erro ao inicializar banco: {result.get_first_error()}")
        
        return result
    
    def register_daily_review(self) -> Result:
        """Registra uma avaliação diária."""
        print("\n📝 REGISTRO DE AVALIAÇÃO DIÁRIA")
        print("=" * 40)
        
        try:
            # Coleta as notas
            work = self._get_note("Trabalho")
            training = self._get_note("Treino")
            studies = self._get_note("Estudos")
            mind = self._get_note("Estado Mental")
            
            # Coleta os comentários
            print("\n💭 COMENTÁRIOS:")
            positive_points = input("Pontos positivos do dia: ").strip()
            negative_points = input("Pontos negativos do dia: ").strip()
            
            # Cria o objeto Review
            review = Review(
                work=work,
                training=training,
                studies=studies,
                mind=mind,
                positive_points=positive_points,
                negative_points=negative_points
            )
            
            # Salva no banco
            result = self.db_service.insert_review(review)
            
            if result.success:
                print(f"\n✅ Avaliação registrada com sucesso!")
                print(f"📊 Média do dia: {review.get_average_score():.1f}/10")
            else:
                print(f"\n❌ Erro ao registrar: {result.get_first_error()}")
            
            return result
            
        except ValueError as e:
            error_msg = f"Dados inválidos: {str(e)}"
            print(f"\n❌ {error_msg}")
            return Result.error_result(error_msg)
        except KeyboardInterrupt:
            print("\n\nOperação cancelada pelo usuário.")
            return Result.error_result("Operação cancelada")
    
    def _get_note(self, category: str) -> int:
        """Solicita uma nota para uma categoria específica."""
        while True:
            try:
                note = int(input(f"{category} (0-10): "))
                if 0 <= note <= 10:
                    return note
                else:
                    print("⚠️  Nota deve estar entre 0 e 10")
            except ValueError:
                print("⚠️  Digite um número válido")
    
    def show_weekly_report(self) -> Result:
        """Mostra o relatório semanal."""
        print("\n📊 RELATÓRIO SEMANAL")
        print("=" * 40)
        
        result = self.db_service.get_weekly_average()
        
        if result.success:
            data = result.data
            print(f"📈 MÉDIAS DA SEMANA:")
            print(f"• Trabalho: {data['avg_work']}/10")
            print(f"• Treino: {data['avg_training']}/10")
            print(f"• Estudos: {data['avg_studies']}/10")
            print(f"• Mente: {data['avg_mind']}/10")
            print(f"\n🎯 MÉDIA GERAL: {data['overall_average']}/10")
            print(f"📅 Total de avaliações: {data['total_reviews']} dias")
        else:
            print(f"❌ {result.get_first_error()}")
        
        return result
    
    def send_weekly_email(self, email: str) -> Result:
        """Envia relatório semanal completo por email."""
        print(f"\n📧 GERANDO RELATÓRIO SEMANAL COMPLETO PARA: {email}")
        
        # Gera relatório completo com IA
        result = self.report_service.generate_weekly_report(email)
        
        if result.success:
            print("✅ Relatório semanal enviado com sucesso!")
            print("🤖 Relatório inclui análise de IA e recomendações personalizadas!")
        else:
            print(f"❌ Erro ao enviar relatório: {result.get_first_error()}")
        
        return result
    
    def show_all_reviews(self) -> Result:
        """Mostra todas as avaliações."""
        print("\n📋 TODAS AS AVALIAÇÕES")
        print("=" * 50)
        
        result = self.db_service.get_all_reviews()
        
        if result.success:
            reviews = result.data
            if not reviews:
                print("Nenhuma avaliação encontrada.")
                return result
            
            for i, review in enumerate(reviews, 1):
                print(f"\n{i}. ID: {review.id}")
                print(f"   Trabalho: {review.work} | Treino: {review.training}")
                print(f"   Estudos: {review.studies} | Mente: {review.mind}")
                print(f"   Média: {review.get_average_score():.1f}")
                print(f"   Positivos: {review.positive_points}")
                print(f"   Negativos: {review.negative_points}")
        else:
            print(f"❌ {result.get_first_error()}")
        
        return result
    
    def run(self):
        """Executa o menu principal da aplicação."""
        print(f"\n🎯 {settings.APP_NAME} v{settings.APP_VERSION}")
        print("=" * 50)
        
        while True:
            print("\n📋 MENU PRINCIPAL:")
            print("1. Registrar avaliação diária")
            print("2. Ver relatório semanal")
            print("3. Ver todas as avaliações")
            print("4. Enviar relatório completo com IA")
            print("5. Sair")
            
            try:
                choice = input("\nEscolha uma opção (1-5): ").strip()
                
                if choice == "1":
                    self.register_daily_review()
                elif choice == "2":
                    self.show_weekly_report()
                elif choice == "3":
                    self.show_all_reviews()
                elif choice == "4":
                    email = input("Digite seu email: ").strip()
                    if email:
                        self.send_weekly_email(email)
                    else:
                        print("❌ Email não pode ser vazio")
                elif choice == "5":
                    print("\n👋 Obrigado por usar o Diário Inteligente!")
                    break
                else:
                    print("❌ Opção inválida. Escolha entre 1 e 5.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Saindo...")
                break
            except Exception as e:
                print(f"\n❌ Erro inesperado: {str(e)}")


def main():
    """Função principal."""
    app = DiarioInteligente()
    
    # Inicializa o banco de dados
    init_result = app.initialize()
    if not init_result.success:
        print("❌ Falha ao inicializar aplicação")
        return
    
    # Executa o menu principal
    app.run()


if __name__ == "__main__":
    main()