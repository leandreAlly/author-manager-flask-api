from flask_mail import Mail, Message
from flask import current_app

mail = Mail()

def send_email(to, subject, template):
  msg = Message(
    subject,
    recipients=[to],
    html = template,
    sender = current_app.config['MAIL_DEFAULT_SENDER']
  )
  mail.send(msg)