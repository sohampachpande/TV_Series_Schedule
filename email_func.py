from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import getpass
import smtplib

server = smtplib.SMTP('smtp.gmail.com', 587)

# log in to the server
username = input('Enter gmail address: ')  
# x@gmail.com'
password = getpass.getpass('Enter Password: ')
# 'x' Disclaimer: Password is not encrypted
server.ehlo()
server.starttls()
server.ehlo()
server.login(username, password)

fromaddr = username
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['Subject'] = "TV Series Schedule"


def send_email(body_content, toaddr):
    msg['To'] = toaddr
    msg.attach(MIMEText(body_content, 'plain'))
    text = msg.as_string()
    # Send mail
    try:
        server.sendmail(fromaddr, toaddr, text)
        return(1)
    # If some error is encountered, print the error details
    except Exception as e:
        print('Error:', e)
        return(e)
