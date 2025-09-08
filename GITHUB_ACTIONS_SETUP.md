# 🤖 Configuração do GitHub Actions

## 📋 Passo a Passo para Configurar

### 1. **Fazer Upload do Banco de Dados**
Como o GitHub Actions não tem acesso ao seu banco local, você precisa:

```bash
# Copie o banco de dados para o repositório
cp data/reviews.db ./reviews.db
```

### 2. **Configurar Secrets no GitHub**

No seu repositório GitHub, vá em:
`Settings` → `Secrets and variables` → `Actions`

Adicione os seguintes secrets:

- **`EMAIL_USER`**: Seu email do Gmail
- **`EMAIL_PASSWORD`**: Sua senha de app do Gmail
- **`WEEKLY_REPORT_EMAIL`**: Email que receberá o relatório

### 3. **Como Obter Senha de App do Gmail**

1. Acesse: https://myaccount.google.com/security
2. Ative a **Verificação em duas etapas**
3. Gere uma **Senha de app** para "Mail"
4. Use essa senha no `EMAIL_PASSWORD`

### 4. **Testar o GitHub Actions**

1. Faça commit e push do código
2. Vá em `Actions` no seu repositório
3. Clique em "Weekly Report - Diário Inteligente"
4. Clique em "Run workflow" para testar

### 5. **Cronograma**

- **Execução**: Todo sábado às 9h (horário de Brasília)
- **Custo**: 100% gratuito
- **Limite**: 2000 minutos/mês (mais que suficiente)

## 🔧 Troubleshooting

### Erro de Email
- Verifique se a senha de app está correta
- Confirme se a verificação em duas etapas está ativa

### Erro de Banco
- Certifique-se que `reviews.db` está no repositório
- Verifique se há dados no banco

### Erro de Permissões
- Verifique se os secrets estão configurados
- Confirme se o workflow está habilitado
