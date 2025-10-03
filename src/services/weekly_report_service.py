"""
Serviço para geração de relatórios semanais automáticos.
Combina dados estatísticos com análise de IA para criar relatórios personalizados.
"""

from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from ..models.result import Result
from ..models.review import Review
from .database_service import DatabaseService
from .email_service import EmailService
from .ai_analysis_service import AIAnalysisService
from ..config.settings import settings


class WeeklyReportService:
    """Serviço para geração e envio de relatórios semanais."""
    
    def __init__(self):
        """Inicializa o serviço de relatório semanal."""
        self.db_service = DatabaseService()
        self.email_service = EmailService()
        self.ai_service = AIAnalysisService()
    
    def generate_weekly_report(self, target_email: Optional[str] = None) -> Result:
        """
        Gera e envia o relatório semanal completo.
        
        Args:
            target_email: Email para envio (se None, usa configuração padrão)
            
        Returns:
            Result: Resultado da operação
        """
        try:
            print("📊 Gerando relatório semanal...")
            
            # 1. Busca dados da semana
            weekly_data_result = self.db_service.get_weekly_average()
            if not weekly_data_result.success:
                return weekly_data_result
            
            weekly_data = weekly_data_result.data
            
            # 2. Busca avaliações da semana para análise
            reviews_result = self._get_weekly_reviews()
            if not reviews_result.success:
                return reviews_result
            
            reviews = reviews_result.data
            
            # 2.1. Verifica se há avaliações na semana
            if not reviews or len(reviews) == 0:
                print("⚠️  Nenhuma avaliação encontrada na semana")
                if target_email:
                    return self._send_no_data_email(target_email)
                else:
                    return Result.success_result({
                        'message': 'Nenhuma avaliação encontrada na semana',
                        'weekly_data': weekly_data,
                        'reviews_count': 0
                    })
            
            # 3. Gera análise com IA
            analysis_result = self.ai_service.analyze_weekly_data(weekly_data, reviews)
            if not analysis_result.success:
                return analysis_result
            
            analysis = analysis_result.data
            
            # 4. Cria o relatório completo
            report = self._create_complete_report(weekly_data, analysis)
            
            # 5. Envia por email se solicitado
            if target_email:
                email_result = self._send_weekly_report(target_email, report)
                if not email_result.success:
                    return email_result
            
            return Result.success_result({
                'report': report,
                'weekly_data': weekly_data,
                'analysis': analysis,
                'email_sent': target_email is not None
            })
            
        except Exception as e:
            return Result.error_result(f"Erro ao gerar relatório semanal: {str(e)}")
    
    def _get_weekly_reviews(self) -> Result:
        """Busca avaliações da última semana."""
        try:
            # Calcula data de uma semana atrás
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            
            print(f"📅 Buscando avaliações de {start_date} até {end_date}")
            
            # Tenta buscar por período, se não conseguir, busca todas
            result = self.db_service.get_reviews_by_date_range(start_date, end_date)
            if not result.success:
                # Se falhar, busca todas as avaliações
                print("⚠️  Buscando todas as avaliações (fallback)")
                result = self.db_service.get_all_reviews()
            
            reviews = result.data if result.success else []
            print(f"📊 Encontradas {len(reviews)} avaliações na semana")
            
            return Result.success_result(reviews)
            
        except Exception as e:
            return Result.error_result(f"Erro ao buscar avaliações da semana: {str(e)}")
    
    def _create_complete_report(self, weekly_data: Dict[str, Any], analysis: Dict[str, Any]) -> str:
        """Cria o relatório completo formatado."""
        
        report = f"""
🎯 {settings.APP_NAME} - RELATÓRIO SEMANAL
{'=' * 50}

{analysis['motivational_message']}

📊 ESTATÍSTICAS DA SEMANA:
• Trabalho: {weekly_data['avg_work']}/10
• Treino: {weekly_data['avg_training']}/10  
• Estudos: {weekly_data['avg_studies']}/10
• Mente: {weekly_data['avg_mind']}/10

🎯 MÉDIA GERAL: {weekly_data['overall_average']}/10
📅 Total de avaliações: {weekly_data['total_reviews']} dias

{analysis['weekly_summary']}

💡 INSIGHTS DA SEMANA:
"""
        
        # Adiciona insights
        for insight in analysis['insights']:
            report += f"• {insight}\n"
        
        report += f"""
🎯 RECOMENDAÇÕES PARA PRÓXIMA SEMANA:
"""
        
        # Adiciona recomendações
        for recommendation in analysis['recommendations']:
            report += f"• {recommendation}\n"
        
        report += f"""
🌟 LEMBRE-SE:
Cada dia é uma nova oportunidade de crescimento. 
Pequenas melhorias diárias levam a grandes transformações!

---
📱 Gerado automaticamente pelo {settings.APP_NAME} v{settings.APP_VERSION}
🕒 {datetime.now().strftime('%d/%m/%Y às %H:%M')}
        """.strip()
        
        return report
    
    def _send_weekly_report(self, email: str, report: str) -> Result:
        """Envia o relatório por email."""
        try:
            subject = f"{settings.APP_NAME} - Relatório Semanal ({datetime.now().strftime('%d/%m/%Y')})"
            
            # Adiciona formatação HTML para melhor visualização
            html_body = self._format_html_email(report)
            
            return self.email_service.send_email(email, subject, html_body)
            
        except Exception as e:
            return Result.error_result(f"Erro ao enviar relatório: {str(e)}")
    
    def _format_html_email(self, report: str) -> str:
        """Formata o relatório para HTML."""
        # Converte quebras de linha para HTML
        html_report = report.replace('\n', '<br>')
        
        # Adiciona estilos básicos
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                {html_report}
            </div>
        </body>
        </html>
        """
        
        return html_body
    
    def schedule_weekly_report(self, target_email: str) -> Result:
        """
        Agenda o envio do relatório semanal.
        Este método será chamado pelo GitHub Actions.
        """
        try:
            print(f"🕒 Executando relatório semanal agendado para: {target_email}")
            
            result = self.generate_weekly_report(target_email)
            
            if result.success:
                print("✅ Relatório semanal enviado com sucesso!")
            else:
                print(f"❌ Erro ao enviar relatório: {result.get_first_error()}")
            
            return result
            
        except Exception as e:
            error_msg = f"Erro no relatório agendado: {str(e)}"
            print(f"❌ {error_msg}")
            return Result.error_result(error_msg)
    
    def _send_no_data_email(self, email: str) -> Result:
        """
        Envia email informando que não há dados da semana.
        
        Args:
            email: Email do destinatário
            
        Returns:
            Result: Resultado da operação
        """
        try:
            subject = f"{settings.APP_NAME} - Sem Avaliações Esta Semana ({datetime.now().strftime('%d/%m/%Y')})"
            
            body = f"""
🎯 {settings.APP_NAME} - RELATÓRIO SEMANAL
{'=' * 50}

📅 Semana de {datetime.now().strftime('%d/%m/%Y')}

⚠️  NENHUMA AVALIAÇÃO ENCONTRADA

Esta semana não foram registradas avaliações diárias.

💡 LEMBRE-SE:
• Formulários são enviados nas segundas, quartas e sextas às 20h
• Responda os emails para registrar suas avaliações
• No sábado você receberá o relatório com análise de IA

📝 PRÓXIMOS PASSOS:
1. Aguarde o próximo formulário (Segunda/Quarta/Sexta)
2. Preencha e responda o email
3. Continue registrando suas avaliações diárias

🌟 Cada avaliação ajuda a IA a dar insights melhores!

---
📱 Gerado automaticamente pelo {settings.APP_NAME} v{settings.APP_VERSION}
🕒 {datetime.now().strftime('%d/%m/%Y às %H:%M')}
            """.strip()
            
            return self.email_service.send_email(email, subject, body)
            
        except Exception as e:
            return Result.error_result(f"Erro ao enviar email sem dados: {str(e)}")
