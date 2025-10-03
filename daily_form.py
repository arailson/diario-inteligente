"""
Script para envio automático de formulários diários.
Este script será executado pelo GitHub Actions nas segundas, quartas e sextas.
"""

import os
import sys
from datetime import datetime

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.services.daily_form_sender import DailyFormService
from src.config.settings import settings


def main():
    """Função principal para envio de formulários diários."""
    print(f"📝 Iniciando envio de formulário diário - {datetime.now()}")
    print(f"📱 {settings.APP_NAME} v{settings.APP_VERSION}")
    
    # Email de destino (configurado via variável de ambiente)
    target_email = os.getenv('DAILY_FORM_EMAIL', 'sapao.vieira@gmail.com')
    
    if not target_email:
        print("❌ Erro: DAILY_FORM_EMAIL não configurado")
        return 1
    
    print(f"📧 Enviando formulário para: {target_email}")
    
    # Inicializa o serviço
    form_service = DailyFormService()
    
    # Verifica se hoje é dia de formulário
    schedule_info = form_service.get_form_schedule_info()
    print(f"📅 Hoje é {schedule_info['current_day']}")
    print(f"📝 É dia de formulário: {schedule_info['is_today_form_day']}")
    
    if not schedule_info['is_today_form_day']:
        print("ℹ️  Hoje não é dia de formulário (Segunda/Quarta/Sexta)")
        print(f"📅 Próximo formulário: {schedule_info['next_form_day']}")
        return 0
    
    # Envia o formulário
    result = form_service.schedule_daily_form(target_email)
    
    if result.success:
        print("✅ Formulário diário enviado com sucesso!")
        print("📝 Responda o email para enviar sua avaliação")
        return 0
    else:
        print(f"❌ Erro no envio: {result.get_first_error()}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
