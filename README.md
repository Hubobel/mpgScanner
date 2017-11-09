
# mpgScanner
holt die Vertretungspläne vom Schulserver und verschickt diese, sollten Aktualisierungen vorliegen, dann per Mail und/oder Telegram-Messenger an beliebige viele
Empfänger (via Blindcopy, BCC),in Abhänigkeit davon, ob gerade Ferien oder ein Feiertag sind.
Für Nutzer der Hausautomation "Homematic": Es wird eine Systemvariable "Ferien" automatisch auf "True" bzw "False" gesetzt, wenn man dies möchte.


# Installation

Das File downloaden und in einen beliebigen Ordner, in welchem man natürlich Schreibrechte besitzen muss, stecken.
Nach dem ersten Start wird automatisch eine Datei pass.json im gleichen Verzeichniss erstellt und die Anwendung beendet sich selbst.
Nun müssen folgende Angaben innerhalb dieser 'pass.json' gemacht werden:

* "gmail_pass":Passwort für den eigenen G-Mail Account (wird zum Versenden der PDF´s benötigt)
* "gmail_user":eigene Emailadresse des für die versendung zuständigen Accounts
* "Land":Europäisches Kürzel für den eignen Wohnort (z.Bsp. RP für RheinlandPfalz)
* "TOKEN":der Usertoken des Telegrammessengers (optional)
* "Chat_ID":Chat_ID des Telegrammessengers (optional)
* "ccu_ip":IP der CCU-Zentrale der Hausautomation 'Homematic' (optional)
* "wetter_API": der API-Key von wunderground.com
* "wetter_Ort": die ID der verwendeten Wetterstation


Weiterhin muss auf dem ausführenden System die Pythonbiliothek "pyTelegramBotAPI" installiert sein (wenn man Telegram nutzen möchte, sonst wird diese Funktion automatisch deaktiviert:

* sollte pip noch nicht installiert sein: "sudo apt-get installe python3-pip"
* pip3 install pyTelegramBotAPI
  
Bsp. für eine leere pass.json, wie sie automatisch nach dem ersten Start angelegt wird:

{
    "Chat_ID": "",
    "Land": "rp",
    "TOKEN": "",
    "ccu_ip": "",
    "gmail_pass": "",
    "gmail_user": "",
    "mpg_pass": "",
    "mpg_user": ""
}
# Benutzung

Das Programm wird am besten über einen Cronjob periodisch aufgerufen, z.Bsp. Stündlich, immer zur halben Stunde, im Zeitraum von 7 bis 15 Uhr, an den Werk(Schul-)tagen Montag bis Freitag.
Eintrag in der crontab sollte dann in etwa so ausschauen (Pfad zum Script bitte anpassen):

30 7-15 * * 1-5 python3 /home/carsten/Scripts/mpgScanner.py

# Disclaimer

Diese Software benutz den Zugang zum Schulserver des Max-Planck-Gymnasiums in Ludwigshafen (http://www.mpglu.de/aktuelles/vertretungsplan.html), um dort die Vertretungspläne für den aktuellen und den darauf folgenden Schultag zu laden. Für die Feier- und Ferientagsdaten wird die API von smartnoob.de  (https://robin.meis.space/2014/04/15/ferien-feiertag-api-fuer-deutschland/) benutz. Vielen Dank für die Bereitstellung der Daten.
Für das "Zitat des Tages Feature" nutze ich die API von https://taeglicheszit.at
Um die aktuelle Temperatur/Luftfeuchtigkeit und "Bedeckung" anzuzeigen, greife ich auf die API von http://www.wunderground.com zurück.



[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.me/Hubobel)
