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
        
                            <!-- CTA Button -->
                            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin: 30px 0;">
                                <tr>
                                    <td align="center">
                                        <a href="{form_url}" style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-decoration: none; padding: 18px 50px; border-radius: 10px; font-size: 18px; font-weight: 600; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);">
                                            📝 Preencher Avaliação
                                        </a>
                                    </td>
                                </tr>
                            </table>
                            
                            <p style="margin: 25px 0 0 0; font-size: 14px; color: #999; text-align: center;">
                                Ou copie e cole este link no seu navegador:<br>
                                <a href="{form_url}" style="color: #667eea; text-decoration: none;">{form_url}</a>
                            </p>
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="padding: 30px; text-align: center; border-top: 1px solid #e1e5e9;">
                            <p style="margin: 0; font-size: 14px; color: #999;">🤖 Enviado automaticamente pelo Diário Inteligente</p>
                            <p style="margin: 10px 0 0 0; font-size: 12px; color: #ccc;">Segunda, Quarta e Sexta às 20:00</p>
                        </td>
                    </tr>
                    
                </table>
            </td>
        </tr>
    </table>
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
