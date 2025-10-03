# 🚀 Como Rodar a Aplicação Web

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Pip instalado
- Variáveis de ambiente configuradas no `.env`

## 🔧 Instalação

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

Isso vai instalar:
- `flask` - Framework web
- `flask-cors` - Suporte para CORS
- `python-dotenv` - Gerenciamento de variáveis de ambiente
- `schedule` - Agendamento de tarefas

### 2. Configurar `.env` (se ainda não configurou)

Crie ou edite o arquivo `.env` na raiz do projeto:

```env
EMAIL_USER=seu-email@gmail.com
EMAIL_PASSWORD=sua-senha-app
```

## ▶️ Como Rodar

### Opção 1: Rodar Diretamente

```bash
python app/app.py
```

### Opção 2: Usar Flask CLI

```bash
cd app
flask run
```

### Opção 3: Rodar com Debug

```bash
export FLASK_ENV=development  # Linux/Mac
set FLASK_ENV=development     # Windows CMD
$env:FLASK_ENV="development"  # Windows PowerShell

python app/app.py
```

## 🌐 Acessar a Aplicação

Após iniciar o servidor, você verá:

```
🚀 Servidor iniciado em http://localhost:5000
📝 Acesse http://localhost:5000/formulario para preencher avaliação
```

### URLs Disponíveis:

- **Página Inicial**: http://localhost:5000/
- **Formulário**: http://localhost:5000/formulario
- **Sucesso**: http://localhost:5000/sucesso
- **Health Check**: http://localhost:5000/health

### Com Parâmetros (simulando email):

```
http://localhost:5000/formulario?email=seu-email@gmail.com&date=03/10/2025
```

## 🧪 Testar a Aplicação

### 1. Testar no Navegador

1. Abra http://localhost:5000/formulario
2. Selecione as notas (0-10) para cada categoria
3. Preencha os pontos positivos e negativos
4. Clique em "Enviar Avaliação"
5. Você será redirecionado para a página de sucesso

### 2. Testar a API (via curl)

```bash
curl -X POST http://localhost:5000/api/submit \
  -H "Content-Type: application/json" \
  -d '{
    "work": 8,
    "training": 7,
    "studies": 9,
    "mind": 8,
    "positive_points": "Dia produtivo!",
    "negative_points": "Preciso melhorar o sono",
    "email": "seu-email@gmail.com"
  }'
```

### 3. Testar Health Check

```bash
curl http://localhost:5000/health
```

## 📊 Verificar Dados Salvos

Após enviar uma avaliação, você pode verificar o banco de dados:

```bash
python -c "from src.services.database_service import DatabaseService; db = DatabaseService(); result = db.get_all_reviews(); print(result.data if result.success else result.errors)"
```

## 🎨 Funcionalidades da Interface

### ✅ O que funciona:

1. **Seleção de Notas**:
   - Clique nos botões de 0 a 10
   - Gradiente de cores (vermelho → amarelo → verde)
   - Feedback visual ao selecionar
   - Animação ao passar o mouse

2. **Campos de Texto**:
   - Pontos positivos
   - Pontos negativos
   - Validação de campos obrigatórios

3. **Validação**:
   - Verifica se todas as notas foram selecionadas
   - Verifica se os campos de texto estão preenchidos
   - Mostra mensagens de erro claras

4. **Envio**:
   - Salva no banco de dados
   - Envia email de confirmação para o usuário
   - Envia notificação para o admin
   - Redireciona para página de sucesso

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'flask'"

**Solução**: Instale as dependências
```bash
pip install -r requirements.txt
```

### Erro: "Address already in use"

**Solução**: Mate o processo na porta 5000
```bash
# Linux/Mac
lsof -ti:5000 | xargs kill -9

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Erro: "No such file or directory: 'data/reviews.db'"

**Solução**: Crie o diretório data
```bash
mkdir -p data
```

O banco de dados será criado automaticamente no primeiro uso.

### JavaScript não funciona

**Solução**: Verifique o console do navegador (F12)
- Deve aparecer "✅ Formulário carregado"
- Deve aparecer "✅ X botões inicializados"

## 🔄 Restart Automático (Desenvolvimento)

Para desenvolvimento, o Flask recarrega automaticamente ao modificar arquivos:

```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
python app/app.py
```

## 🚀 Próximos Passos

### Para Deploy em Produção:

1. **Usar um servidor WSGI**:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app.app:app
   ```

2. **Configurar HTTPS**

3. **Usar variáveis de ambiente corretas**

4. **Configurar domínio real**

5. **Atualizar `FORM_URL` no `.env`**

## 📝 Notas Importantes

- **Porta padrão**: 5000
- **Debug mode**: Ativado por padrão no desenvolvimento
- **Auto-reload**: Ativado no modo debug
- **CORS**: Habilitado para desenvolvimento

## 🆘 Suporte

Se encontrar problemas:
1. Verifique os logs no terminal
2. Verifique o console do navegador (F12)
3. Verifique se todas as dependências estão instaladas
4. Verifique se o `.env` está configurado

---

**Desenvolvido com ❤️ para o Diário Inteligente**

