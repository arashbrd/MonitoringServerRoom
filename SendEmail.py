
import smtplib
from email.mime.multipart import MIMEMultipart
# from email.MIMEMultipart import MIMEMultipart
from email.mime.text import MIMEText
from Utils import SaveErrorLog

# from smtplib import SMTP_SSL as SMTP       # this invokes the secure SMTP protocol (port 465, uses SSL)

def SendEmail(TOemailAdress,Subject,Message):
    try:

        msg = MIMEMultipart()

        password = "---"
        msg['From'] = ---@---"
        msg['To'] = TOemailAdress
        msg['Subject'] = Subject

        message = Message
        msg.attach( MIMEText(message, 'plain') )

        server = smtplib.SMTP('0.0.0.0)
        # server.starttls()

        server.login(msg['From'], password)

        server.sendmail( msg['From'], msg['To'], msg.as_string() )
        txt='Email sent FROM '+msg['From']+' TO '+msg['To'] +' AS ' +msg.as_string()
        SaveErrorLog(txt)
        server.quit()
    except:
        pass

