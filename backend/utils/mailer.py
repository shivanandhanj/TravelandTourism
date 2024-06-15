import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(to, subject, text, html):
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = 'shyamsaran0206@gmail.com'
        msg['To'] = to
        msg['Subject'] = subject
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        msg.attach(part1)
        msg.attach(part2)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('shyamsaran0206@gmail.com', 'vyki efil wiww ybav')

        server.sendmail('shyamsaran0206@gmail.com', to, msg.as_string())

        server.quit()

        print('Message sent')
        return 'Email sent successfully'
    except Exception as e:
        print(e)
        raise Exception('Error sending email')
    
# send_email('recipient@example.com', 'Subject', 'Plain text body', '<h1>HTML body</h1>')
