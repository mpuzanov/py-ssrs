"""
Модуль по работе с электронной почтой
"""
import smtplib
import ssl
from os.path import basename

from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from ssrs.config import settings, logger


def get_body_text(file):
    """ Возвращает текст для тела письма email сообщения """
    return f"""<html><body><p>Добрый день.<br>К письму прикреплен отчет: {file}</p></body></html>"""


def send_email(to_addr, body_text, subject, attach_files: str = "") -> bool:
    """
    Функция отправки Email
    :param to_addr: кому
    :param body_text: текст сообщения
    :param subject: тема письма
    :param attach_files: список вложенных файлов через ';'
    :return: True или False
    """
    port = settings.mail_port
    smtp_server = settings.mail_server
    sender_email = settings.mail_username
    password = settings.mail_password

    msg = MIMEMultipart()
    msg['To'] = to_addr
    msg['From'] = sender_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body_text, "html" if 'html' in body_text else "plain"))

    # =====================================================================
    # Формируем список вложенных файлов для отправки
    files_to_attach = [x.strip() for x in attach_files.split(';') if x != '']

    for file_to_attach in files_to_attach:
        # прикладываем файлы
        attachment = MIMEBase('application', "octet-stream")
        try:
            with open(file_to_attach, "rb") as fh:
                attachment.set_payload(fh.read())

            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition', 'attachment', filename=basename(file_to_attach))
            msg.attach(attachment)
        except IOError:
            msg = f"Error opening attachment file {file_to_attach}"
            raise RuntimeError(msg)
    # ==============================================================

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL(smtp_server, port, context=context, timeout=settings.mail_timeout) as server:
            server.login(sender_email, password)
            sendmail_status = server.sendmail(
                sender_email, to_addr, msg.as_string()
            )
            if sendmail_status != {}:
                logger.error(f'error send email to {to_addr}: {sendmail_status=}')
            return True
    except Exception as error:
        logger.error(f'\n{error=}')
        return False
