"""
Template de email para notificação de formulário diário.
Envia email com link para formulário web.
"""

def create_notification_email_html(date: str, form_url: str) -> str:
    """
    Cria o HTML do email de notificação com link para o formulário.
    
    Args:
        date: Data da avaliação (ex: "08/10/2025")
        form_url: URL para acessar o formulário web
        
    Returns:
        HTML do email de notificação
    """
    
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Diário Inteligente - Hora da Avaliação!</title>
</head>
<body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f5f5f5;">
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f5f5f5; padding: 40px 20px;">
        <tr>
            <td align="center">
                <table width="600" cellpadding="0" cellspacing="0" border="0" style="background-color: white; border-radius: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.1);">
                    
                    <!-- Header -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 30px; text-align: center; border-radius: 15px 15px 0 0;">
                            <h1 style="margin: 0; font-size: 32px; color: white;">🎯 Diário Inteligente</h1>
                            <p style="margin: 15px 0 0 0; font-size: 18px; color: rgba(255,255,255,0.9);">Hora da sua avaliação diária!</p>
                        </td>
                    </tr>
                    
                    <!-- Content -->
                    <tr>
                        <td style="padding: 40px 30px;">
                            <h2 style="margin: 0 0 20px 0; font-size: 24px; color: #333;">📅 Avaliação de {date}</h2>
                            
                            <p style="margin: 0 0 25px 0; font-size: 16px; color: #666; line-height: 1.6;">
                                Olá! É hora de registrar como foi o seu dia. Clique no botão abaixo para acessar o formulário de avaliação diária.
                            </p>
                            
                            <!-- Tips Box -->
                            <div style="background-color: #f8f9fa; border-left: 4px solid #667eea; padding: 20px; margin: 25px 0; border-radius: 0 10px 10px 0;">
                                <h3 style="margin: 0 0 15px 0; font-size: 18px; color: #667eea;">💡 Dicas para uma boa avaliação:</h3>
                                <ul style="margin: 0; padding-left: 20px; color: #666; line-height: 1.8;">
                                    <li>Seja honesto com suas notas (0-10)</li>
                                    <li>Pense no dia como um todo</li>
                                    <li>Detalhe os pontos positivos e negativos</li>
                                    <li>Leva apenas 2-3 minutos!</li>
            </ul>
        </div>
        
        <div style="background: #d4edda; color: #155724; padding: 15px; border-radius: 8px; margin-bottom: 20px; text-align: center; display: none;" id="successMessage">
            ✅ Avaliação enviada com sucesso! Você receberá uma confirmação por email.
        </div>
        
        <form id="evaluationForm">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 40px; margin-bottom: 25px;">
                <div style="margin-bottom: 30px;">
                    <div style="text-align: center; margin-bottom: 20px;">
                        <span style="font-size: 40px; display: block; margin-bottom: 10px;">💼</span>
                        <h3 style="margin: 0; color: #333; font-size: 20px; font-weight: 600;">Trabalho</h3>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; padding: 0 10px;">
                        <span style="font-size: 14px; color: #666; font-weight: 500;">0</span>
                        <span style="font-size: 14px; color: #666; font-weight: 500;">1</span>
                        <span style="font-size: 14px; color: #666; font-weight: 500;">2</span>
                        <span style="font-size: 14px; color: #666; font-weight: 500;">3</span>
                        <span style="font-size: 14px; color: #666; font-weight: 500;">4</span>
                        <span style="font-size: 14px; color: #666; font-weight: 500;">5</span>
                        <span style="font-size: 14px; color: #666; font-weight: 500;">6</span>
                        <span style="font-size: 14px; color: #666; font-weight: 500;">7</span>
                        <span style="font-size: 14px; color: #666; font-weight: 500;">8</span>
                        <span style="font-size: 14px; color: #666; font-weight: 500;">9</span>
                        <span style="font-size: 14px; color: #666; font-weight: 500;">10</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; padding: 0 5px;">
                        <input type="radio" name="work" value="0" style="transform: scale(1.5); cursor: pointer;" required>
                        <input type="radio" name="work" value="1" style="transform: scale(1.5); cursor: pointer;" required>
                        <input type="radio" name="work" value="2" style="transform: scale(1.5); cursor: pointer;" required>
                        <input type="radio" name="work" value="3" style="transform: scale(1.5); cursor: pointer;" required>
                        <input type="radio" name="work" value="4" style="transform: scale(1.5); cursor: pointer;" required>
                        <input type="radio" name="work" value="5" style="transform: scale(1.5); cursor: pointer;" required>
                        <input type="radio" name="work" value="6" style="transform: scale(1.5); cursor: pointer;" required>
                        <input type="radio" name="work" value="7" style="transform: scale(1.5); cursor: pointer;" required>
                        <input type="radio" name="work" value="8" style="transform: scale(1.5); cursor: pointer;" required>
                        <input type="radio" name="work" value="9" style="transform: scale(1.5); cursor: pointer;" required>
                        <input type="radio" name="work" value="10" style="transform: scale(1.5); cursor: pointer;" required>
                    </div>
                </div>
                
                <div style="margin-bottom: 30px;">
                    <div style="text-align: center; margin-bottom: 20px;">
                        <span style="font-size: 40px; display: block; margin-bottom: 10px;">🏃‍♂️</span>
                        <h3 style="margin: 0; color: #333; font-size: 20px; font-weight: 600;">Treino</h3>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; padding: 0 10px;">
                        <span style="font-size: 14px; color: #666; font-weight: 500;">0</span>
                        <span style="font-size: 14px; color: #666; font-weight: 500;">1</span>
                        <span style="font-size: 14px; color: #666; font-weight: 500;">2</span>
                        <span style="font-size: 14px; color: #666; font-weight: 500;">3</span>
                        <span style="font-size: 14px; color: #666; font-weight: 500;">4</span>
                        <span style="font-size: 14px; color: #666; font-weight: 500;">5</span>
                        <span style="font-size: 14px; color: #666; font-weight: 500;">6</span>
                        <span style="font-size: 14px; color: #666; font-weight: 500;">7</span>
                        <span style="font-size: 14px; color: #666; font-weight: 500;">8</span>
                        <span style="font-size: 14px; color: #666; font-weight: 500;">9</span>
                        <span style="font-size: 14px; color: #666; font-weight: 500;">10</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; padding: 0 5px;">
                        <input type="radio" name="training" value="0" style="transform: scale(1.5); cursor: pointer;" required>
                        <input type="radio" name="training" value="1" style="transform: scale(1.5); cursor: pointer;" required>
                        <input type="radio" name="training" value="2" style="transform: scale(1.5); cursor: pointer;" required>
                        <input type="radio" name="training" value="3" style="transform: scale(1.5); cursor: pointer;" required>
                        <input type="radio" name="training" value="4" style="transform: scale(1.5); cursor: pointer;" required>
                        <input type="radio" name="training" value="5" style="transform: scale(1.5); cursor: pointer;" required>
                        <input type="radio" name="training" value="6" style="transform: scale(1.5); cursor: pointer;" required>
                        <input type="radio" name="training" value="7" style="transform: scale(1.5); cursor: pointer;" required>
                        <input type="radio" name="training" value="8" style="transform: scale(1.5); cursor: pointer;" required>
                        <input type="radio" name="training" value="9" style="transform: scale(1.5); cursor: pointer;" required>
                        <input type="radio" name="training" value="10" style="transform: scale(1.5); cursor: pointer;" required>
                    </div>
                </div>
                
                <div style="margin-bottom: 30px;">
                    <div style="text-align: center; margin-bottom: 20px;">
                        <span style="font-size: 40px; display: block; margin-bottom: 10px;">📚</span>
                        <h3 style="margin: 0; color: #333; font-size: 20px; font-weight: 600;">Estudos</h3>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; padding: 0 10px;">
                        <span style="font-size: 14px; color: #666; font-weight: 500;">0</span>
                        <span style="font-size: 14px; color: #666; font-weight: 500;">1</span>
                        <span style="font-size: 14px; color: #666; font-weight: 500;">2</span>
                        <span style="font-size: 14px; color: #666; font-weight: 500;">3</span>
                        <span style="font-size: 14px; color: #666; font-weight: 500;">4</span>
                        <span style="font-size: 14px; color: #666; font-weight: 500;">5</span>
                        <span style="font-size: 14px; color: #666; font-weight: 500;">6</span>
                        <span style="font-size: 14px; color: #666; font-weight: 500;">7</span>
                        <span style="font-size: 14px; color: #666; font-weight: 500;">8</span>
                        <span style="font-size: 14px; color: #666; font-weight: 500;">9</span>
                        <span style="font-size: 14px; color: #666; font-weight: 500;">10</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; padding: 0 5px;">
                        <input type="radio" name="studies" value="0" style="transform: scale(1.5); cursor: pointer;" required>
                        <input type="radio" name="studies" value="1" style="transform: scale(1.5); cursor: pointer;" required>
                        <input type="radio" name="studies" value="2" style="transform: scale(1.5); cursor: pointer;" required>
                        <input type="radio" name="studies" value="3" style="transform: scale(1.5); cursor: pointer;" required>
                        <input type="radio" name="studies" value="4" style="transform: scale(1.5); cursor: pointer;" required>
                        <input type="radio" name="studies" value="5" style="transform: scale(1.5); cursor: pointer;" required>
                        <input type="radio" name="studies" value="6" style="transform: scale(1.5); cursor: pointer;" required>
                        <input type="radio" name="studies" value="7" style="transform: scale(1.5); cursor: pointer;" required>
                        <input type="radio" name="studies" value="8" style="transform: scale(1.5); cursor: pointer;" required>
                        <input type="radio" name="studies" value="9" style="transform: scale(1.5); cursor: pointer;" required>
                        <input type="radio" name="studies" value="10" style="transform: scale(1.5); cursor: pointer;" required>
                    </div>
                </div>
                
                <div style="margin-bottom: 30px;">
                    <div style="text-align: center; margin-bottom: 20px;">
                        <span style="font-size: 40px; display: block; margin-bottom: 10px;">🧠</span>
                        <h3 style="margin: 0; color: #333; font-size: 20px; font-weight: 600;">Estado Mental</h3>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; padding: 0 10px;">
                        <span style="font-size: 14px; color: #666; font-weight: 500;">0</span>
                        <span style="font-size: 14px; color: #666; font-weight: 500;">1</span>
                        <span style="font-size: 14px; color: #666; font-weight: 500;">2</span>
                        <span style="font-size: 14px; color: #666; font-weight: 500;">3</span>
                        <span style="font-size: 14px; color: #666; font-weight: 500;">4</span>
                        <span style="font-size: 14px; color: #666; font-weight: 500;">5</span>
                        <span style="font-size: 14px; color: #666; font-weight: 500;">6</span>
                        <span style="font-size: 14px; color: #666; font-weight: 500;">7</span>
                        <span style="font-size: 14px; color: #666; font-weight: 500;">8</span>
                        <span style="font-size: 14px; color: #666; font-weight: 500;">9</span>
                        <span style="font-size: 14px; color: #666; font-weight: 500;">10</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; padding: 0 5px;">
                        <input type="radio" name="mind" value="0" style="transform: scale(1.5); cursor: pointer;" required>
                        <input type="radio" name="mind" value="1" style="transform: scale(1.5); cursor: pointer;" required>
                        <input type="radio" name="mind" value="2" style="transform: scale(1.5); cursor: pointer;" required>
                        <input type="radio" name="mind" value="3" style="transform: scale(1.5); cursor: pointer;" required>
                        <input type="radio" name="mind" value="4" style="transform: scale(1.5); cursor: pointer;" required>
                        <input type="radio" name="mind" value="5" style="transform: scale(1.5); cursor: pointer;" required>
                        <input type="radio" name="mind" value="6" style="transform: scale(1.5); cursor: pointer;" required>
                        <input type="radio" name="mind" value="7" style="transform: scale(1.5); cursor: pointer;" required>
                        <input type="radio" name="mind" value="8" style="transform: scale(1.5); cursor: pointer;" required>
                        <input type="radio" name="mind" value="9" style="transform: scale(1.5); cursor: pointer;" required>
                        <input type="radio" name="mind" value="10" style="transform: scale(1.5); cursor: pointer;" required>
                    </div>
                </div>
            </div>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 25px;">
                <div style="margin-bottom: 20px;">
                    <label for="positive_points" style="display: block; margin-bottom: 8px; font-weight: 600; color: #333; font-size: 16px;">
                        <span style="font-size: 20px; margin-right: 8px;">✨</span>Pontos Positivos
                    </label>
                    <textarea id="positive_points" name="positive_points" style="width: 100%; padding: 15px; border: 2px solid #e1e5e9; border-radius: 8px; font-size: 16px; resize: vertical; min-height: 100px; box-sizing: border-box;" placeholder="Descreva os pontos positivos do seu dia..." required></textarea>
                </div>
                
                <div style="margin-bottom: 20px;">
                    <label for="negative_points" style="display: block; margin-bottom: 8px; font-weight: 600; color: #333; font-size: 16px;">
                        <span style="font-size: 20px; margin-right: 8px;">📉</span>Pontos Negativos
                    </label>
                    <textarea id="negative_points" name="negative_points" style="width: 100%; padding: 15px; border: 2px solid #e1e5e9; border-radius: 8px; font-size: 16px; resize: vertical; min-height: 100px; box-sizing: border-box;" placeholder="Descreva os pontos que podem melhorar..." required></textarea>
                </div>
            </div>
            
            <button type="button" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; padding: 18px 40px; border-radius: 10px; font-size: 18px; font-weight: 600; cursor: pointer; width: 100%; transition: all 0.3s ease;" onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 10px 25px rgba(102, 126, 234, 0.3)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none'" onclick="this.style.transform='translateY(-1px)'">
                📤 Enviar Avaliação
            </button>
        </form>
        
        <div style="text-align: center; margin-top: 30px; color: #666; font-size: 14px;">
            <p>🤖 Gerado automaticamente pelo Diário Inteligente</p>
            <p>📧 Sua avaliação será processada automaticamente</p>
        </div>
    </div>
    
</body>
</html>"""


def format_daily_form_email(date: str, time: str, form_url: str) -> str:
    """
    Formata o email de notificação com link para formulário.
    
    Args:
        date: Data atual (ex: "08/10/2025")
        time: Horário atual (ex: "20:00") - não usado atualmente
        form_url: URL para acessar o formulário web
        
    Returns:
        HTML formatado do email de notificação
    """
    return create_notification_email_html(date, form_url)
