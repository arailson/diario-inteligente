import schedule
import time
from src.database import create_table, insert_data, consult_data
from src.email_utils import send_email
from src.results import Results

# results_create_table = create_table()
# print("results_create_table:", results_create_table)

# results_insert_data = insert_data(10, 7, 3, 6, "Some positive points", "Some negative points")

# if results_insert_data.success:
#     result = consult_data()
    
#     print("Retorno sucesso: ", result.data)
    
# else:
#     print("Erro ao inserir dados:", results_insert_data)





# subject = "Teste de envio de e-mail"
# body = "Este é um e-mail de teste enviado automaticamente."
# to_email = "arailson.vieira@gmail.com"

# result_email = send_email(subject, body, to_email)
# print(result_email)

def generate_weekly_report():
    try:
        return Results(success=True, data="Mensagem de teste relatorio semanal")
    except Exception as e:
        return Results(success=False, error_message=[str(e)])


def send_weekly_email():
    try:
        subject = "Relatório Semanal"
        body = generate_weekly_report().data
        to_email = "arailson.vieira@gmail.com"
        
        result = send_email(subject, body, to_email)
        
        if result.success:
            print(result.data)
        else:
            print(f"Error: {', '.join(result.error_message)}") 
        
        return Results(success=True, data=result.data)
    except Exception as e:
        return Results(success=False, error_message=[str(e)])


# Agendar para todo sábado às 9:00 AM    
schedule.every().saturday.at("12:00").do(send_weekly_email)

# Loop para executar o agendamento
while True:
    schedule.run_pending()  # Executa as tarefas agendadas
    time.sleep(60)