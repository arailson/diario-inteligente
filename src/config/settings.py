"""
Configurações centralizadas do projeto.
Todas as configurações ficam em um lugar só, facilitando a manutenção.
"""

import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()


class Settings:
    """Classe para gerenciar todas as configurações do projeto."""
    
    # Configurações do banco de dados
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'data/reviews.db')
    
    # Configurações de email
    EMAIL_USER = os.getenv('EMAIL_USER')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    EMAIL_SMTP_SERVER = os.getenv('EMAIL_SMTP_SERVER', 'smtp.gmail.com')
    EMAIL_SMTP_PORT = int(os.getenv('EMAIL_SMTP_PORT', '587'))
    
    # Configurações da aplicação
    APP_NAME = "Diário Inteligente"
    APP_VERSION = "2.0.0"
    
    @classmethod
    def validate_email_settings(cls) -> bool:
        """Verifica se as configurações de email estão completas."""
        return all([
            cls.EMAIL_USER,
            cls.EMAIL_PASSWORD
        ])
    
    @classmethod
    def get_database_url(cls) -> str:
        """Retorna a URL completa do banco de dados."""
        return f"sqlite:///{cls.DATABASE_PATH}"
    
    @classmethod
    def print_config(cls):
        """Imprime as configurações atuais (sem senhas)."""
        print(f"=== {cls.APP_NAME} v{cls.APP_VERSION} ===")
        print(f"Database: {cls.DATABASE_PATH}")
        print(f"Email User: {cls.EMAIL_USER}")
        print(f"SMTP Server: {cls.EMAIL_SMTP_SERVER}:{cls.EMAIL_SMTP_PORT}")
        print(f"Email configured: {cls.validate_email_settings()}")


# Instância global das configurações
settings = Settings()
