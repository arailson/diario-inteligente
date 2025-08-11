from src.database import create_table, insert_data, consult_data
from src.email import send_email

# results_create_table = create_table()
# print("results_create_table:", results_create_table)

# results_insert_data = insert_data(10, 7, 3, 6, "Some positive points", "Some negative points")

# if results_insert_data.success:
#     result = consult_data()
    
#     print("Retorno sucesso: ", result.data)
    
# else:
#     print("Erro ao inserir dados:", results_insert_data)



subject = "Teste de envio de e-mail"
body = "Este é um e-mail de teste enviado automaticamente."
to_email = "arailson.vieira@gmail.com"

result_email = send_email(subject, body, to_email)
print(result_email)
