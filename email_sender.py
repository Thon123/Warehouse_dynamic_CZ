#!/usr/bin/python3
#Pro účely zasílání emailu v případě, kdy nějaká část selže

import smtplib
from email.mime.text import MIMEText
from datetime import datetime

def posli_email(predmet, prijemce):
    """Funkce pro zasílání emailu"""
    cas = datetime.utcnow().strftime("%H:%M")
    smtp_ssl_host = 'smtp.unknown.cz'
    smtp_ssl_port = 465
    username = 'username'
    password = 'password'
    sender = 'robert.kanera@yescom.cz'
    msg = MIMEText(f"Warehouse_updater failure:\n{predmet}:{cas}")
    msg['Subject'] = (f"{predmet}: {cas}")
    msg['From'] = sender
    msg['To'] = prijemce
    server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
    server.login(username, password)
    server.sendmail(sender, prijemce, msg.as_string())
    server.quit()