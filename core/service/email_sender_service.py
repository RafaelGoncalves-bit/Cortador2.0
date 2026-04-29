import json
import smtplib
from email.message import EmailMessage
import ssl

class EmailSender:
    def __init__(self):
        with open("../utils/email_config.json", "r") as f:
            self.SMTP = json.load(f)

    def send_email(self, subject: str, body: str) -> None:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = self.SMTP["username"]
        msg["To"] = self.SMTP["destinatario"]
        msg.set_content(body)

        contexto = ssl.create_default_context()
        with smtplib.SMTP(self.SMTP["host"], self.SMTP["port"], timeout=10) as server:
            server.starttls(context=contexto)
            server.login(self.SMTP["username"], self.SMTP["password"])
            server.send_message(msg)
            
# enviarEmail = EmailSender()
# enviarEmail.send_email(
#     "Teste", "Teste"
# )