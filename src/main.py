from src.database import create_table, insert_data, consult_data

create_table()

insert_data(8, 7, 9, 6, 'Treinei bem hoje', 'Foquei no trabalho hoje')

data = consult_data()
print(data)