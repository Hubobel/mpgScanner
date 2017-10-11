import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

pfad = os.path.dirname(__file__)

def Nachricht(fradress, toadress, bccs=[], sub='I am ROOT',body='this comes from Hubobel', attach=[]):
    fromaddr = fradress
    toaddr = toadress

    fobj = open(pfad + "/mpg/pass.txt")     #Passwort für den Gmailaccount laden
    passw = []
    for line in fobj:
        a = line.rstrip()
        passw.append(a)
    fobj.close()
    pwd = passw[0]

    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = sub

    msg.attach(MIMEText(body, 'plain'))

    for each in attach:

        filename = each
        attachment = open(pfad + '/mpg/'+each, 'rb')

        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename= %s' % filename)

        msg.attach(part)


    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, pwd)
    text = msg.as_string()
    server.sendmail(fromaddr, bccs, text)
    server.quit()
    return


fobj = open(pfad + "/mpg/adressen.txt")
fradress='carsten.richter77@gmail.com'
toadress='carsten.richter77@gmail.com'
sub='das ist der finale Standalonetest'
anhang = ['adressen.txt','heute.pdf']
body = 'lalaland_Teil2'
bcc = []
for line in fobj:
    a = line.rstrip()
    bcc.append(a)
fobj.close()

Nachricht (fradress,toadress)
