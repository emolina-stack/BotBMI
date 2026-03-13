from email.message import EmailMessage
from dotenv import load_dotenv
import os
import smtplib
import ssl

load_dotenv()
def enviar_correo_error(
    email_from: str = os.getenv("EMAIL_FROM"),
    email_recibe: str = os.getenv("EMAIL_TO"),
    password: str = os.getenv("EMAIL_PASSWORD"),
    subject: str = "Fallo en ejecucion de bot",
    body: str = "Ejecucion del bot fallida.\n\nRevisa la versiones de chrome.\n\nAbre cualquier navegador y en la barra de direcciones ingresa la siguiente url: brave://version/ y valida la version de chrome y luego ejecuta el bot nuevamente. ",
) -> None:


    em = EmailMessage()
    em["From"] = email_from
    em["To"] = email_recibe
    em["Subject"] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_from, password)
        smtp.sendmail(email_from, email_recibe, em.as_string())
