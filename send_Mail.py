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
    if bccs==[]:
        bccs = toadress

    fobj = open(pfad + "/pass.txt")     #Passwort für den Gmailaccount laden
    passw = []
    for line in fobj:
        a = line.rstrip()
        passw.append(a)
    fobj.close()
    pwd = passw[0]
    acc = passw[1]

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
    server.login(acc, pwd)
    text = msg.as_string()
    server.sendmail(fromaddr, bccs, text)
    server.quit()
    return

if os.path.isfile(pfad+'/mpg/adressen.txt')== True:

    fobj = open(pfad + "/mpg/adressen.txt")
    bcc = []
    for line in fobj:
        a = line.rstrip()
        bcc.append(a)
    fobj.close()

fradress='carsten.richter77@gmail.com'
toadress='carsten@hubobel.de'
sub='das ist der finale Standalonetest'
anhang = ['adressen.txt','heute.pdf','morgen.pdf']
body = 'lalaland_Teil3'


Nachricht (fradress,toadress,bcc,'pdfs','und da sind sie',anhang)
print (body+'gdsjfd'+ str(bcc))