"""
Serviço para envio de formulários diários de avaliação.
Envia emails com formulários HTML nas segundas, quartas e sextas.
"""

from datetime import datetime, timedelta
from typing import List
from ..models.result import Result
from .email_service import EmailService
from .daily_form_service import format_daily_form_email
from ..config.settings import settings


class DailyFormService:
    """Serviço para envio de formulários diários."""
    
    def __init__(self):
        """Inicializa o serviço de formulários diários."""
        self.email_service = EmailService()
        self.target_email = None
    
    def send_daily_form(self, target_email: str) -> Result:
        """
        Envia o formulário de avaliação diária.
        
        Args:
            target_email: Email que receberá o formulário
            
        Returns:
            Result: Resultado da operação
        """
        try:
            self.target_email = target_email
            
            # Obtém data e horário atual
            now = datetime.now()
            date_str = now.strftime("%d/%m/%Y")
            time_str = now.strftime("%H:%M")
            
            # Cria o assunto do email
            subject = f"📝 Diário Inteligente - Avaliação Diária ({date_str})"
            
            # URL do formulário web (você precisará configurar isso)
            form_url = f"https://seu-dominio.com/formulario?email={target_email}&date={date_str}"
            
            # Gera o HTML do email de notificação
            html_body = format_daily_form_email(date_str, time_str, form_url)
            
            # Envia o email HTML
            result = self.email_service.send_html_email(target_email, subject, html_body)
            
            if result.success:
                print(f"✅ Formulário diário enviado para: {target_email}")
                print(f"📅 Data: {date_str} às {time_str}")
            else:
                print(f"❌ Erro ao enviar formulário: {result.get_first_error()}")
            
            return result
            
        except Exception as e:
            return Result.error_result(f"Erro ao enviar formulário diário: {str(e)}")
    
    def is_daily_form_day(self) -> bool:
        """
        Verifica se hoje é um dia para envio de formulário.
        Segunda (0), Quarta (2), Sexta (4)
        
        Returns:
            bool: True se é dia de formulário
        """
        today = datetime.now().weekday()
        return today in [0, 2, 4]  # Segunda, Quarta, Sexta
    
    def get_next_form_day(self) -> str:
        """
        Retorna a próxima data de envio de formulário.
        
        Returns:
            str: Próxima data no formato dd/mm/yyyy
        """
        today = datetime.now()
        
        # Dias da semana: Segunda=0, Terça=1, Quarta=2, Quinta=3, Sexta=4, Sábado=5, Domingo=6
        form_days = [0, 2, 4]  # Segunda, Quarta, Sexta
        
        # Procura o próximo dia de formulário
        for days_ahead in range(1, 8):  # Próximos 7 dias
            next_day = today + timedelta(days=days_ahead)
            if next_day.weekday() in form_days:
                return next_day.strftime("%d/%m/%Y")
        
        return "Não encontrado"
    
    def schedule_daily_form(self, target_email: str) -> Result:
        """
        Agenda o envio do formulário diário.
        Este método será chamado pelo GitHub Actions.
        
        Args:
            target_email: Email que receberá o formulário
            
        Returns:
            Result: Resultado da operação
        """
        try:
            print(f"📅 Verificando se hoje é dia de formulário...")
            
            if not self.is_daily_form_day():
                print("ℹ️  Hoje não é dia de formulário (Segunda/Quarta/Sexta)")
                return Result.success_result("Não é dia de formulário")
            
            print(f"📝 Enviando formulário diário para: {target_email}")
            
            result = self.send_daily_form(target_email)
            
            if result.success:
                print("✅ Formulário diário enviado com sucesso!")
            else:
                print(f"❌ Erro ao enviar formulário: {result.get_first_error()}")
            
            return result
            
        except Exception as e:
            error_msg = f"Erro no formulário agendado: {str(e)}"
            print(f"❌ {error_msg}")
            return Result.error_result(error_msg)
    
    def get_form_schedule_info(self) -> dict:
        """
        Retorna informações sobre o cronograma de formulários.
        
        Returns:
            dict: Informações do cronograma
        """
        return {
            'is_today_form_day': self.is_daily_form_day(),
            'next_form_day': self.get_next_form_day(),
            'form_days': ['Segunda-feira', 'Quarta-feira', 'Sexta-feira'],
            'form_time': '20:00',
            'current_day': datetime.now().strftime("%A")
        }
