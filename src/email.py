import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from src.results import Results
from dotenv import load_dotenv

load_dotenv() 

def send_email(subject, body, to_email):
    try:
        from_email = os.getenv('EMAIL_USER')
        from_password = os.getenv('EMAIL_PASSWORD')
        
        if not subject:
            return Results(success=False, error_message=["subject não pode ser vazio"])
        
        if not body:
            return Results(success=False, error_message=["body não pode ser vazio"])
        
        if not to_email:
            return Results(success=False, error_message=["to_email não pode ser vazio"])
            
        
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Corpo do e-mail
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Criptografia
        server.login(from_email, from_password)  # Login na conta
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)  # Envio do e-mail
        server.quit() 
        
        return Results(success=True, data="E-mail enviado com sucesso!")
    
    except Exception as e:
        return Results(success=False, error_message=[str(e)])
        