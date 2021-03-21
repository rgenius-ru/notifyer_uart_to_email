import smtplib
import ssl
import csv
import logging

logger = logging.getLogger('notifier_uart_to_email')  # Create a custom logger

port = 587  # For starttls
smtp_server = "smtp.mail.ru"
sender_email = "notifyer.test1@mail.ru"
password = '3Uap(aYTpaU9'  # input("Type your password and press enter:")

default_message = """
Неизвестная ошибка
"""

pc_str = '[PC program Mail sender]'


def send_email(receiver_email, _message):
    if not _message:
        _message = default_message
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        try:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, _message)
        except smtplib.SMTPException as err:
            logger.error(err, exc_info=False, extra={'email: ': receiver_email})


def notify_all(_message):
    with open("contacts.csv") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for name, email, grade in reader:
            print(pc_str, f"Отправка письма: {name}")
            send_email(email, _message)