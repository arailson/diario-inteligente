"""
Serviço para envio de confirmação de avaliação.
Envia email de confirmação quando uma avaliação é recebida.
"""

from datetime import datetime
from typing import Dict, Any
from ..models.result import Result
from ..models.review import Review
from .email_service import EmailService
from ..config.settings import settings


class ConfirmationService:
    """Serviço para envio de confirmações de avaliação."""
    
    def __init__(self):
        """Inicializa o serviço de confirmação."""
        self.email_service = EmailService()
    
    def send_evaluation_confirmation(self, review: Review, user_email: str) -> Result:
        """
        Envia confirmação de avaliação recebida.
        
        Args:
            review: Avaliação recebida
            user_email: Email do usuário que enviou
            
        Returns:
            Result: Resultado da operação
        """
        try:
            # Cria o assunto
            date_str = datetime.now().strftime('%d/%m/%Y')
            subject = f"✅ Confirmação - Avaliação Recebida ({date_str})"
            
            # Cria o corpo do email
            body = self._create_confirmation_body(review, date_str)
            
            # Envia o email
            result = self.email_service.send_email(user_email, subject, body)
            
            if result.success:
                print(f"✅ Confirmação enviada para: {user_email}")
            else:
                print(f"❌ Erro ao enviar confirmação: {result.get_first_error()}")
            
            return result
            
        except Exception as e:
            return Result.error_result(f"Erro ao enviar confirmação: {str(e)}")
    
    def _create_confirmation_body(self, review: Review, date_str: str) -> str:
        """Cria o corpo do email de confirmação."""
        
        # Calcula a média
        average = review.get_average_score()
        
        # Determina o nível de performance
        if average >= 8.5:
            performance = "🌟 Excepcional"
            emoji = "🎉"
        elif average >= 7.0:
            performance = "👍 Boa"
            emoji = "😊"
        elif average >= 5.5:
            performance = "📊 Regular"
            emoji = "😐"
        else:
            performance = "📈 Melhorar"
            emoji = "💪"
        
        body = f"""
🎯 {settings.APP_NAME} - CONFIRMAÇÃO DE AVALIAÇÃO
{'=' * 50}

{emoji} Sua avaliação foi recebida com sucesso!

📅 Data: {date_str}
🕒 Horário: {datetime.now().strftime('%H:%M')}

📊 SUAS NOTAS:
• 💼 Trabalho: {review.work}/10
• 🏃‍♂️ Treino: {review.training}/10
• 📚 Estudos: {review.studies}/10
• 🧠 Estado Mental: {review.mind}/10

🎯 MÉDIA GERAL: {average:.1f}/10
📈 Performance: {performance}

✨ PONTOS POSITIVOS:
{review.positive_points}

📉 PONTOS NEGATIVOS:
{review.negative_points}

🤖 PRÓXIMOS PASSOS:
• Sua avaliação foi salva no sistema
• No sábado você receberá o relatório semanal
• A IA analisará seus padrões e dará insights

💡 DICA:
Continue registrando suas avaliações diárias para ter insights mais precisos!

---
📱 Gerado automaticamente pelo {settings.APP_NAME} v{settings.APP_VERSION}
🕒 {datetime.now().strftime('%d/%m/%Y às %H:%M')}
        """.strip()
        
        return body
    
    def send_admin_notification(self, review: Review, user_email: str) -> Result:
        """
        Envia notificação para o administrador sobre nova avaliação.
        
        Args:
            review: Avaliação recebida
            user_email: Email do usuário que enviou
            
        Returns:
            Result: Resultado da operação
        """
        try:
            # Email do administrador (você pode configurar)
            admin_email = settings.EMAIL_USER  # Usa o mesmo email configurado
            
            # Cria o assunto
            date_str = datetime.now().strftime('%d/%m/%Y')
            subject = f"📊 Nova Avaliação Recebida - {user_email} ({date_str})"
            
            # Cria o corpo do email
            body = self._create_admin_notification_body(review, user_email, date_str)
            
            # Envia o email
            result = self.email_service.send_email(admin_email, subject, body)
            
            if result.success:
                print(f"📧 Notificação enviada para admin: {admin_email}")
            else:
                print(f"❌ Erro ao enviar notificação: {result.get_first_error()}")
            
            return result
            
        except Exception as e:
            return Result.error_result(f"Erro ao enviar notificação: {str(e)}")
    
    def _create_admin_notification_body(self, review: Review, user_email: str, date_str: str) -> str:
        """Cria o corpo do email de notificação para admin."""
        
        average = review.get_average_score()
        
        body = f"""
📊 {settings.APP_NAME} - NOTIFICAÇÃO DE NOVA AVALIAÇÃO
{'=' * 55}

📅 Data: {date_str}
🕒 Horário: {datetime.now().strftime('%H:%M')}
👤 Usuário: {user_email}

📊 AVALIAÇÃO RECEBIDA:
• 💼 Trabalho: {review.work}/10
• 🏃‍♂️ Treino: {review.training}/10
• 📚 Estudos: {review.studies}/10
• 🧠 Estado Mental: {review.mind}/10

🎯 MÉDIA: {average:.1f}/10

✨ PONTOS POSITIVOS:
{review.positive_points}

📉 PONTOS NEGATIVOS:
{review.negative_points}

📈 STATUS:
• Avaliação salva no banco de dados
• Confirmação enviada para o usuário
• Será incluída no próximo relatório semanal

---
📱 Sistema: {settings.APP_NAME} v{settings.APP_VERSION}
🕒 {datetime.now().strftime('%d/%m/%Y às %H:%M')}
        """.strip()
        
        return body
