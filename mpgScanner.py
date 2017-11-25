import requests
import json
import time
import datetime
import os
import smtplib
import random
import shutil
try:
    import telebot
    telegram = True
except ImportError:
    print('Librarie "telebot" ist nicht installiert. Keine Verwendung von Telegram!!!')
    print('Installation über: "pip3 install pyTelegramBotAPI"')
    telegram = False
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def Download(url):
    #return None
    filename = pfad+'/mpg/'+url+'.pdf'
    url = 'http://www.mpglu.de/vps/'+url+'.pdf'
    req = requests.get(url, auth=(jsonpass['mpg_user'], jsonpass['mpg_pass']))
    file = open(filename, 'wb')
    for chunk in req.iter_content(100000):
        file.write(chunk)
    file.close()
    return None
def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)
def Nachricht(fradress, toadress, bccs=[], sub='I am ROOT',body='this comes from Hubobel', attach=[]):
    fromaddr = fradress
    toaddr = toadress
    if bccs==[]:
        bccs = toadress

    pwd = jsonpass['gmail_pass']
    acc = jsonpass['gmail_user']

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
def json_pass_holen(pfad):
    with open(pfad+'/pass.json') as file:
        passw = json.load(file)
    passw['Uhrzeit'] = time.strftime("%H:%M:%S")
    passw['Tag_Name'] = time.strftime('%A')
    #passw['Tag_Nummer'] = time.strftime('%w')
    passw['pfad']=pfad
    with open(pfad+'/pass.json', 'w') as fp:
        json.dump(passw, fp, sort_keys=True, indent=4)
    return passw
def update():
    global jsonpass
    with open(pfad+'/pass.json') as file:
        jsonpass=json.load(file)
    if 'Tag_Nummer' in jsonpass or jsonpass['debug']=='True':
        print (jsonpass['Tag_Nummer'])
        if jsonpass['Tag_Nummer']!= wtag or jsonpass['debug']=="True":
            print ('update json mit '+str(wtag))
            jsonpass['Tag_Nummer']=str(wtag)
            url_zitat = 'https://taeglicheszit.at/zitat-api.php?format=json'
            resp_zitat = requests.get(url_zitat)
            data_zitat = resp_zitat.json()
            jsonpass['zitat']=data_zitat['zitat']
            jsonpass['autor']=data_zitat['autor']
            with open(pfad+'/pass.json', 'w') as fp:
                json.dump(jsonpass, fp, sort_keys=True, indent=4)
            return True, jsonpass
        else:
            print('kein Update')
            return False
    else:
        jsonpass['Tag_Nummer']=''
        with open(pfad+'/pass.json', 'w') as fp:
            json.dump(jsonpass, fp, sort_keys=True, indent=4)
def Wetter():
    url = 'http://api.wunderground.com/api/'+jsonpass['wetter_API']+'/conditions/lang:DL/q/Germany/pws:'+jsonpass['wetter_Ort']+'.json'
    response = requests.get(url)
    data_response = response.json()
    temperatur=(data_response['current_observation']['temp_c'])
    wetter=(data_response['current_observation']['weather'])
    feuchte=(data_response['current_observation']['relative_humidity'])
    return temperatur,wetter,feuchte
def Chuckfact():
    url_zitat = 'http://api.hubobel.de/zufall'
    resp_zitat = requests.get(url_zitat)
    data_zitat = resp_zitat.json()
    for i in data_zitat:
        fact=(data_zitat[i])
        return fact
def Lotto():
    a = (sorted(random.sample(range(1, 49), 6)))
    b = random.randrange(0, 9)
    while b in a:
        b = random.randrange(1, 49)
    lotto =  str(a) + ',Superzahl: ' + str(b)
    return lotto

pfad = os.path.dirname(__file__)
mail = 0
jetzt = int(time.strftime('%j'))
tag = time.strftime('%d')
wtag = time.strftime('%w')
mailzusatz=""
ferien = False
ferien_morgen = False
feiertag = False
feiertag_morgen = False
fradress='carsten.richter77@gmail.com'
toadress='carsten@hubobel.de'
tage=['Montag','Dienstag','Mittwoch','Donnerstag','Freitag','Samstag','Sonntag']
heute_name=(tage[int(wtag)-1])
if int(wtag)>=5:
    wtag=0
morgen_name=(tage[int(wtag)])

if os.path.isfile(pfad+'/pass.json') !=True:
    print('"pass.json" scheint es nicht zu geben.')
    print('Ich lege eine neue Datei "pass.json" an.')
    passw={"gmail_pass": "","gmail_user": "",
           "mpg_user": "",
           "mpg_pass": "",
           "Chat_ID": "","TOKEN": "",
           "ccu_ip": "","Land": "rp",
           "Wochentag": ""}
    print(str(passw)+ ' bitte entsprechend befüllen.')
    with open(pfad+'/pass.json', 'w') as fp:
        json.dump(passw, fp, sort_keys=True, indent=4)
    quit()
else:
    jsonpass = json_pass_holen(pfad)
if jsonpass['TOKEN']=='' or jsonpass['Chat_ID']=='':
    telegram=False
if telegram:
    TOKEN = jsonpass['TOKEN']
    chat_id = jsonpass['Chat_ID']
    tb = telebot.TeleBot(TOKEN)
if os.path.isfile(pfad+'/mpg/adressen.txt'):
    fobj = open(pfad + "/mpg/adressen.txt")
    bcc = []
    for line in fobj:
        a = line.rstrip()
        bcc.append(a)
    fobj.close()

if jsonpass['ccu_ip']!='':
    url_ferien_ccu = 'http://'+jsonpass['ccu_ip']+'/loksoft.exe?ret=dom.GetObject("Ferien").State('
    ccu = True
else:
    ccu = False

if os.path.isdir(pfad+'/mpg')!= True:   #prüfen, ob das UNTERverzeichniss /mpg bereits existiert
    os.makedirs(pfad+'/mpg')
    print ('Downloadverzeichniss bei '+pfad +' /mpg/ created!!!')

if int(tag) == 1 and int(time.strftime('%H'))== 8:       #Update einmal pro Monat (Ferien)
    print("It´s Update Time!!!")
    url_ferien = 'http://api.smartnoob.de/ferien/v1/ferien/?bundesland=' + jsonpass['Land']
    url_feiertage = 'http://api.smartnoob.de/ferien/v1/feiertage/?bundesland=' + jsonpass['Land']
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
    url_ferien = 'http://api.smartnoob.de/ferien/v1/ferien/?bundesland=' + jsonpass['Land']
    url_feiertage = 'http://api.smartnoob.de/ferien/v1/feiertage/?bundesland=' + jsonpass['Land']
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
    if jetzt-1 == beginn:
        ferien_morgen = True
    if jetzt >= beginn and jetzt <= ende-1:
        ferien_morgen = True
    x = x+1

if ferien and ccu:          #setzen der CCU Variable
    try:
        requests.post(url_ferien_ccu+'1)')
    except:
        None
if ferien == False and ccu :
    try:
        requests.post(url_ferien_ccu+'0)')
    except:
        None

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
    if jetzt+1 == beginn:
        feiertag_morgen = True
    x = x+1

print('Es sind Ferien: '+ str(ferien))
print('Es sind morgen Ferien: '+ str(ferien_morgen))
print('Es ist ein Feiertag: '+str(feiertag))
print('Es ist morgen ein Feiertag: '+str(feiertag_morgen))

if feiertag_morgen:
    mailzusatz = '\n \nMorgen ist ein Feiertag.\nNeue Nachrichten erst am nächsten Werktag wieder.\nGenießt die Zeit!'
############################################################
if ferien:
    print('Es sind Ferien, also lass ich euch in Ruhe')
    quit()
if feiertag_morgen:
    print('Morgen ist Feiertag, also gibts auch nichts, was sich lohnt, anzuschauen.')
    #quit()

try:
    os.rename(pfad + '/mpg/heute.pdf', pfad +'/mpg/heute1.pdf')
    url = 'heute'
    Download(url)
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
    Download(url)

try:
    os.rename(pfad+'/mpg/morgen.pdf', pfad+'/mpg/morgen1.pdf')
    url = 'morgen'
    Download(url)
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
    Download(url)

#sub='Hier kommt der Betreff rein'
#body = 'hier der Mailtext'
#anhang = ['adressen.txt','heute.pdf','morgen.pdf']
#Nachricht (fradress,toadress,bcc,sub,body,anhang)

if mail!=0 or jsonpass['debug']=='True':
    if update():
        print ('Neuer Tag, neues Gluck!')
        if wtag == '1':
            mailzusatz = '\n \nWillkommen in der ' + str(time.strftime('%W')) + '.Kalenderwoche.' + \
                         '\nNicht verzagen, nur Druck formt aus Kohle einen Diamanten!' \
                         '\nZitat des Tages:\n'+ jsonpass['zitat']+ \
                         '\nAutor: ' + jsonpass['autor'] + '\n'
        if wtag == '2':
            mailzusatz = '\n \nDer Montag liegt hinter uns.\nAb heuteb kann es  nur noch aufwärts gehen!' \
                         '\nViel Spass, bei allem, was ihr so treibt\n'+ \
                         '\nZitat des Tages:\n'+ jsonpass['zitat']+ \
                         "\nAutor: " + jsonpass['autor'] + '\n'
        if wtag == '3':
            lotto=Lotto()
            mailzusatz = '\n \nHallo Mittwoch!\nIch wünsche eine schöne Wochenmitte.\nKopf hoch! ' \
                         + 'Wenn ich Lotto spielen würde, dann kämen heute folgende Zahlen zum Einsatz: ' +lotto +\
                         '\n\nZitat des Tages:\n'+ jsonpass['zitat']+ \
                         "\nAutor: " + jsonpass['autor'] + '\n'
        if wtag == '4':
            mailzusatz = '\n \nDer Donnerstag ist bekanntlich der \'kleine Freitag\'' \
                         '\nNur noch einmal (!) Gas geben!\n' '\nZitat des Tages:\n'+ jsonpass['zitat']+\
                         '\nAutor: '+jsonpass['autor']+'\n'
        if wtag == '5':
            lotto=Lotto()
            mailzusatz = '\n \nEs ist Freitag!\nIch wünsche ein schönes Wochenende.' \
                         '\nNeue Nachrichten kommen erst am Montag wieder.\n'+'Vieleicht habt ihr ja am Samstag'\
                        ' Glück beim Lotto. Probiert doch mal diese Zahlen: '+lotto+\
                         '\n\nZitat des Tages:\n'+ jsonpass['zitat']+\
                         '\nAutor: '+jsonpass['autor']+'\n'
    else:
        print ('im Westen nix neues')

if jsonpass['debug']=="True":
    update()
    print('DEBUG_MODE')
    bcc=jsonpass['debug_adress']
    TOKEN = jsonpass['debug_TOKEN']
    chat_id = jsonpass['debug_Chat_ID']
    tb = telebot.TeleBot(TOKEN)
    mailzusatz = mailzusatz + '\n \nDies ist eine Testnachricht!\nDer Versand erfolgt nur an Hubobel und schneeschieben.\n\n' \
                 'Zitat des Tages:\n'+ jsonpass['zitat']+'\nAutor: '+jsonpass['autor']+'\n'
if 'wetter_API' in jsonpass:
    if jsonpass['wetter_API']!='':
        temperatur,wetter,feuchte=Wetter()
        bericht='\nAktuell haben wir geschmeidige '+str(temperatur)+' Grad Celsius bei '+str(feuchte)\
                +' Luftfeuchtigkeit.\nDer Himmel ist '+str(wetter)+'.\n'
    else:
        bericht = 'Wie das Wetter derzeit ist? Man(n) richte seinen Blick gen Himmel oder' \
                  ' generiere einen API-Key unter https://www.wunderground.com/signup?mode=api_signup'
else:
    bericht='Wie das Wetter derzeit ist? Man(n) richte seinen Blick gen Himmel oder' \
            ' generiere einen API-Key unter https://www.wunderground.com/signup?mode=api_signup'
fact='\nChuck-Norris-Fact:\n'+Chuckfact()

shutil.copy(pfad+'/mpg/morgen.pdf',pfad+'/mpg/'+morgen_name+'.pdf')

if mail == 1 or jsonpass['debug']=='True':
    body = 'Es gibt eine aktuelle Version des heutigen Vertretungsplanes.'+mailzusatz+bericht+fact
    anhang = ['heute.pdf']
    sub = 'MPG-heute aktualisiert'
    if os.path.isfile(pfad + '/mpg/adressen.txt'):
        Nachricht(fradress, toadress, bcc, sub, body, anhang)
        print (body+' ich versende das mal an: '+str(bcc))
    if telegram:
        document = open(pfad+'/mpg/heute.pdf', 'rb')
        tb.send_document(chat_id, document, caption='Es gibt eine aktuelle Version des heutigen Vertretungsplanes.')
        tb.send_message(chat_id, mailzusatz+bericht+fact)
if mail == 2 or jsonpass['debug']=='True':
    body = 'Es gibt eine aktualisierte Version des Vertretungsplanes für '+morgen_name+mailzusatz+bericht+fact
    anhang = [morgen_name+'.pdf']
    sub = 'MPG-morgen aktualisiert'
    if os.path.isfile(pfad + '/mpg/adressen.txt'):
        Nachricht(fradress, toadress, bcc, sub, body, anhang)
        print (body+' ich versende das mal an: '+str(bcc))
    if telegram:
        document = open(pfad + '/mpg/'+morgen_name+'.pdf', 'rb')
        tb.send_document(chat_id, document, caption='Es gibt eine aktualisierte Version '
                                                    'des Vertretungsplanes für '+morgen_name+'.')
        tb.send_message(chat_id, mailzusatz + bericht+fact)
if mail == 3 or jsonpass['debug']=='True':
    body = 'Es gibt aktualisierte Versionen der MPG-Vertretungspläne.'+mailzusatz+bericht+fact
    anhang = ['heute.pdf',morgen_name+'.pdf']
    sub = 'MPG-Vertretungspläne aktualisiert'
    if os.path.isfile(pfad + '/mpg/adressen.txt'):
        Nachricht(fradress, toadress, bcc, sub, body, anhang)
        print (body+' ich versende das mal an: '+str(bcc))
    if telegram:
        document = open(pfad + '/mpg/heute.pdf', 'rb')
        tb.send_document(chat_id, document, caption='Es gibt aktualisierte Versionen der MPG-Vertretungspläne.')
        document = open(pfad + '/mpg/'+morgen_name+'.pdf', 'rb')
        tb.send_document(chat_id, document)
        tb.send_message(chat_id, mailzusatz + bericht+fact)

