import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(to_name,to_email,from_name, from_email, subject, msg):
    MESSAGE = MIMEMultipart('alternative')
    MESSAGE['subject'] = subject
    MESSAGE['To'] = to_name
    MESSAGE['From'] = from_name
    BODY=msg
    HTML_BODY = MIMEText(BODY, 'html')
    MESSAGE.attach(HTML_BODY)
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login('noednikretep@gmail.com','zkxvcglowagvbuqq') 
    server.sendmail(from_email, to_email,MESSAGE.as_string())
    server.quit()
    return 0