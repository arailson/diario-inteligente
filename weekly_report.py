"""
Script para execução automática do relatório semanal.
Este script será executado pelo GitHub Actions todo sábado.
"""

import os
import sys
from datetime import datetime

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.services.weekly_report_service import WeeklyReportService
from src.config.settings import settings


def main():
    """Função principal para execução automática."""
    print(f"🤖 Iniciando execução automática - {datetime.now()}")
    print(f"📱 {settings.APP_NAME} v{settings.APP_VERSION}")
    
    # Email de destino (você pode configurar via variável de ambiente)
    target_email = os.getenv('WEEKLY_REPORT_EMAIL', 'sapao.vieira@gmail.com')
    
    if not target_email:
        print("❌ Erro: WEEKLY_REPORT_EMAIL não configurado")
        return 1
    
    print(f"📧 Enviando relatório para: {target_email}")
    
    # Inicializa o serviço
    report_service = WeeklyReportService()
    
    # Executa o relatório
    result = report_service.schedule_weekly_report(target_email)
    
    if result.success:
        print("✅ Relatório semanal executado com sucesso!")
        return 0
    else:
        print(f"❌ Erro na execução: {result.get_first_error()}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
