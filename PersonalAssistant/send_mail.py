import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# environment varialbles
username = 'mailmepms@gmail.com'
password = 'rog@531gt'

def send_mail(text='Email Body', subject='Hello World', from_email='PMS <mailmepms@gmail.com>',  to_emails=None, html=None):
    assert isinstance(to_emails, list)
    msg = MIMEMultipart('alternative')
    msg['from'] = from_email
    msg['to'] = ", ".join(to_emails)
    msg['Subject'] = subject
    txt_part = MIMEText(text, 'plain')
    msg.attach(txt_part)
    if html != None:
        html_part = MIMEText("<h1>This is working</h1>", 'html')
        msg.attach(html_part)

    msg_str = msg.as_string() 

    # login to my smtp server
    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(from_email, to_emails, msg_str)

    server.quit()
    # with smtplib.SMTP() as server:
    #     server.login()
    #     pass
