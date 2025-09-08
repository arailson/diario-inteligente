"""
Serviço para envio de emails.
Centraliza todas as operações relacionadas ao envio de emails.
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict, Any
from ..models.result import Result
from ..config.settings import settings


class EmailService:
    """Classe para gerenciar o envio de emails."""
    
    def __init__(self):
        """Inicializa o serviço de email."""
        self.smtp_server = settings.EMAIL_SMTP_SERVER
        self.smtp_port = settings.EMAIL_SMTP_PORT
        self.email_user = settings.EMAIL_USER
        self.email_password = settings.EMAIL_PASSWORD
    
    def _validate_email_settings(self) -> Result:
        """Valida se as configurações de email estão completas."""
        if not self.email_user:
            return Result.error_result("EMAIL_USER não configurado")
        
        if not self.email_password:
            return Result.error_result("EMAIL_PASSWORD não configurado")
        
        return Result.success_result()
    
    def send_email(self, to_email: str, subject: str, body: str) -> Result:
        """
        Envia um email.
        
        Args:
            to_email (str): Email do destinatário
            subject (str): Assunto do email
            body (str): Corpo do email
            
        Returns:
            Result: Resultado da operação
        """
        try:
            # Valida configurações
            config_result = self._validate_email_settings()
            if not config_result.success:
                return config_result
            
            # Valida parâmetros
            validation_result = self._validate_email_params(to_email, subject, body)
            if not validation_result.success:
                return validation_result
            
            # Cria a mensagem
            msg = MIMEMultipart()
            msg['From'] = self.email_user
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Adiciona o corpo do email
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # Conecta e envia
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()  # Habilita criptografia
            server.login(self.email_user, self.email_password)
            
            text = msg.as_string()
            server.sendmail(self.email_user, to_email, text)
            server.quit()
            
            return Result.success_result("Email enviado com sucesso!")
            
        except smtplib.SMTPAuthenticationError:
            return Result.error_result("Erro de autenticação. Verifique usuário e senha.")
        except smtplib.SMTPRecipientsRefused:
            return Result.error_result("Email do destinatário inválido.")
        except smtplib.SMTPException as e:
            return Result.error_result(f"Erro SMTP: {str(e)}")
        except Exception as e:
            return Result.error_result(f"Erro ao enviar email: {str(e)}")
    
    def _validate_email_params(self, to_email: str, subject: str, body: str) -> Result:
        """Valida os parâmetros do email."""
        errors = []
        
        if not to_email or not isinstance(to_email, str) or not to_email.strip():
            errors.append("Email do destinatário não pode ser vazio")
        
        if not subject or not isinstance(subject, str) or not subject.strip():
            errors.append("Assunto não pode ser vazio")
        
        if not body or not isinstance(body, str) or not body.strip():
            errors.append("Corpo do email não pode ser vazio")
        
        # Validação básica de formato de email
        if to_email and '@' not in to_email:
            errors.append("Formato de email inválido")
        
        if errors:
            return Result.error_result_multiple(errors)
        
        return Result.success_result()
    
    def send_weekly_report(self, to_email: str, weekly_data: Dict[str, Any]) -> Result:
        """
        Envia relatório semanal por email.
        
        Args:
            to_email (str): Email do destinatário
            weekly_data (Dict): Dados da semana
            
        Returns:
            Result: Resultado da operação
        """
        try:
            subject = f"{settings.APP_NAME} - Relatório Semanal"
            
            # Monta o corpo do email
            body = self._create_weekly_report_body(weekly_data)
            
            return self.send_email(to_email, subject, body)
            
        except Exception as e:
            return Result.error_result(f"Erro ao enviar relatório semanal: {str(e)}")
    
    def _create_weekly_report_body(self, weekly_data: Dict[str, Any]) -> str:
        """Cria o corpo do relatório semanal."""
        body = f"""
{settings.APP_NAME} - Relatório Semanal

Olá! Aqui está seu relatório semanal:

📊 MÉDIAS DA SEMANA:
• Trabalho: {weekly_data['avg_work']}/10
• Treino: {weekly_data['avg_training']}/10
• Estudos: {weekly_data['avg_studies']}/10
• Mente: {weekly_data['avg_mind']}/10

🎯 MÉDIA GERAL: {weekly_data['overall_average']}/10

📈 TOTAL DE AVALIAÇÕES: {weekly_data['total_reviews']} dias

---
Este é um relatório automático do {settings.APP_NAME}.
Continue registrando suas avaliações diárias!

Versão: {settings.APP_VERSION}
        """.strip()
        
        return body
