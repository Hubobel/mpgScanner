import requests
import json
import time
import datetime
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


pfad = os.path.dirname(__file__)
mail = 0
url_ferien ='http://api.smartnoob.de/ferien/v1/ferien/?bundesland=rp'
url_feiertage = 'http://api.smartnoob.de/ferien/v1/feiertage/?bundesland=rp'

jetzt = int(time.strftime('%j'))
tag = time.strftime('%d')

ferien = False
ferien_morgen = False
feiertag = False
feiertag_morgen = False


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


if os.path.isdir(pfad+'/mpg')!= True:   #prüfen, ob das UNTERverzeichniss /mpg bereits existiert
    os.makedirs(pfad+'/mpg')
    print ('Downloadverzeichniss bei '+pfad +' /mpg/ created!!!')

if int(tag) == 1:       #Update einmal pro Monat
    print("It´s Update Time!!!")
    resp_ferien = requests.get(url_ferien)
    resp_feiertage = requests.get(url_feiertage)
    data_ferien = resp_ferien.json()
    data_feiertage = resp_feiertage.json()

    with open(pfad + '/mpg/json_ferien.data', 'w') as outfile:
        json.dump(data_ferien, outfile)

    with open(pfad + '/mpg/json_feiertage.data', 'w') as outfile:
        json.dump(data_feiertage, outfile)

if os.path.isfile(pfad+'/mpg/json_ferien.data')!= True:     #Download der jsons, falls diese lokal nicht existieren
    print('The json_xxx.datas not found, will try to download them from the API')

    resp_ferien = requests.get(url_ferien)
    resp_feiertage = requests.get(url_feiertage)
    data_ferien = resp_ferien.json()
    data_feiertage = resp_feiertage.json()

    with open(pfad+'/mpg/json_ferien.data','w') as outfile:
        json.dump(data_ferien, outfile)

    with open(pfad+'/mpg/json_feiertage.data','w') as outfile:
        json.dump(data_feiertage, outfile)

with open(pfad+'/mpg/json_ferien.data') as file:
    data_ferien=json.load(file)
with open(pfad+'/mpg/json_feiertage.data') as file:
    data_feiertage=json.load(file)

a= len(data_ferien['daten'])
x = 0

while x <a:
    beginn = data_ferien['daten'][x]['beginn']
    beginn = datetime.datetime.fromtimestamp(beginn)
    beginn = int(beginn.strftime('%j'))

    ende = data_ferien['daten'][x]['ende']
    ende = datetime.datetime.fromtimestamp(ende)
    ende = int(ende.strftime('%j'))-1

    if jetzt <= ende and jetzt >= beginn:
        ferien = True
        ferien_morgen = True
    if jetzt-1 == beginn:
        ferien_morgen = True

    x = x+1

a= len(data_feiertage['daten'])
x = 0

while x <a:
    beginn = data_feiertage['daten'][x]['beginn']
    beginn = datetime.datetime.fromtimestamp(beginn)
    beginn = int(beginn.strftime('%j'))

    ende = data_feiertage['daten'][x]['ende']
    ende = datetime.datetime.fromtimestamp(ende)
    ende = int(ende.strftime('%j'))-1

    if jetzt <= ende and jetzt >= beginn:
        feiertag = True
    if jetzt-1 == beginn:
        feiertag_morgen = True
    x = x+1

print('Es sind Ferien: '+ str(ferien))
print('Es sind morgen Ferien: '+ str(ferien_morgen))
print('Es ist ein Feiertag: '+str(feiertag))
print('Es ist morgen ein Feiertag: '+str(feiertag_morgen))

feiertag=False
feiertag_morgen=False
ferien_morgen=False
ferien=False
############################################################
if ferien or ferien_morgen:
    quit()
if feiertag or feiertag_morgen:
    quit()

def download(url):
    #return None
    filename = pfad+'/mpg/'+url+'.pdf'
    url = 'http://www.mpglu.de/vps/'+url+'.pdf'
    req = requests.get(url, auth=('schueler', 'Ing8gresk'))
    file = open(filename, 'wb')
    for chunk in req.iter_content(100000):
        file.write(chunk)
    file.close()
    return None

def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)


try:
    os.rename(pfad + '/mpg/heute.pdf', pfad +'/mpg/heute1.pdf')
    url = 'heute'
    download(url)
    x = os.stat(pfad+'/mpg/heute.pdf')
    x = x.st_size
    x1 = str(x)
    y = os.stat(pfad+'/mpg/heute1.pdf')
    y = y.st_size
    y1 = str(y)


    if x != y:
        mail=mail+1
    else:
        print("Es gibt keine neuen Mals mit 'heute'")
        d = modification_date(pfad+'/mpg/heute.pdf')
        d = d.strftime('%H:%M:%S')
        print("heute: " + d + ' '+ x1 + ' Bytes')
        d = modification_date(pfad+'/mpg/heute1.pdf')
        d = d.strftime('%H:%M:%S')
        print("heute1: " + d + ' '+ y1 + ' Bytes')
except FileNotFoundError:
    print("File Heute.PDF not found")
    print("Will try to download it from the MPG-Server")
    url = 'heute'
    download(url)

try:
    os.rename(pfad+'/mpg/morgen.pdf', pfad+'/mpg/morgen1.pdf')
    url = 'morgen'
    download(url)
    x = os.stat(pfad+'/mpg/morgen.pdf')
    x = x.st_size
    x1 = str(x)
    y = os.stat(pfad+'/mpg/morgen1.pdf')
    y = y.st_size
    y1 = str(y)
    if x != y:
        mail = mail + 2
    else:
        print("Es gibt keine neuen Mails mit 'morgen'")

        d= modification_date(pfad+'/mpg/morgen.pdf')
        d = d.strftime('%H:%M:%S')
        print("morgen: " + d + ' ' + x1 + ' Bytes')
        d = modification_date(pfad+'/mpg/morgen1.pdf')
        d = d.strftime('%H:%M:%S')
        print("morgen1: " + d + ' ' + x1 + ' Bytes')
except FileNotFoundError:
    print("File Morgen.PDF not found")
    print("Will try to download it from the MPG-Server")
    url = 'morgen'
    download(url)




if os.path.isfile(pfad+'/mpg/adressen.txt')== True:

    fobj = open(pfad + "/mpg/adressen.txt")
    bcc = []
    for line in fobj:
        a = line.rstrip()
        bcc.append(a)
    fobj.close()

fradress='carsten.richter77@gmail.com'
toadress='carsten@hubobel.de'
#sub='das ist der erste Kombitest'
#body = 'lalaland_Teil3'
#anhang = ['adressen.txt','heute.pdf','morgen.pdf']
#Nachricht (fradress,toadress,bcc,sub,body,anhang)
mail=3

if mail == 1:
    body = 'Es gibt eine aktuelle Version des heutigen Vertretungsplanes.'
    anhang = ['heute.pdf']
    sub = 'MPG-heute aktualisiert'
    Nachricht(fradress, toadress, bcc, sub, body, anhang)

if mail == 2:
    body = 'Es gibt eine aktuelle Version des morgigen Vertretungsplanes.'
    anhang = ['morgen.pdf']
    sub = 'MPG-morgen aktualisiert'
    Nachricht(fradress, toadress, bcc, sub, body, anhang)
if mail == 3:
    body = 'Es gibt aktuelle Versionen der MPG-Vertretungspläne.'
    anhang = ['heute.pdf','morgen.pdf']
    sub = 'MPG-Vertretungspläne aktualisiert'
    Nachricht(fradress, toadress, bcc, sub, body, anhang)