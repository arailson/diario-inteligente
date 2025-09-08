# Diário Inteligente

Este é um projeto pessoal para registrar e avaliar o meu dia a dia, atribuindo notas a diferentes aspectos da minha rotina (trabalho, treino, estudos e mente). O projeto também gera um feedback semanal, baseado nas notas, e envia por e-mail.

## Estrutura do Projeto

```
diario-inteligente/
├── src/
│   ├── models/          # Classes de dados e modelos
│   │   ├── __init__.py
│   │   ├── review.py    # Modelo de avaliação diária
│   │   └── result.py    # Classe para resultados de operações
│   ├── services/        # Lógica de negócio
│   │   ├── __init__.py
│   │   ├── database_service.py  # Operações de banco de dados
│   │   └── email_service.py     # Envio de emails
│   ├── config/          # Configurações
│   │   ├── __init__.py
│   │   └── settings.py  # Configurações centralizadas
│   └── main.py          # Arquivo principal
├── data/               # Dados do banco
├── requirements.txt
└── README.md
```

## Funcionalidades:
- Registrar notas diárias para diferentes áreas
- Gerar uma média semanal das notas
- Enviar feedback automático por e-mail

## Como usar:
1. Configure as variáveis de ambiente no arquivo `.env`
2. Execute `python src/main.py`