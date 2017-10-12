
# mpgScanner
holt die Vertretungspläne vom Schulserver und verschickt diese, sollten Aktualisierungen vorliegen, dann per Mail an beliebige viele
Empfänger (via Blindcopy, BCC),in Abhänigkeit davon, ob gerade Ferien oder ein Feiertag sind.
Für Nutzer der Hausautomation "Homematic": Es wird eine Systemvariable "Ferien" automatisch auf "True" bzw "False" gesetzt, wenn man dies möchte.


# Installation

Das File downloaden und in einen beliebigen Ordner, in welchem man natürlich Schreibrechte besitzen muss, stecken.
Im gleichen Ordner muss eine neue Datei, mit dem Namen 'pass.txt', erstellt werden.
Hierin werden nun Zeilenweise die folgenden Angaben gemacht:

- Passwort für den eigenen G-Mail Account (wird zum Versenden der PDF´s benötigt)
- eigene Emailadresse des für die versendung zuständigen Accounts
- Europäisches Kürzel für den eignen Wohnort (wird zur Ermittlung der Feier- und Ferientage benötigt. z.Bsp. RP für RheinlandPfalz)

Weiterhin muss auf dem ausführenden System die Pythonbiliothek "pyTelegramBotAPI" installiert sein (wenn man Telegram nutzen möchte, sonst wird diese Funktion automatisch deaktiviert:

  -sollte pip noch nicht installiert sein: "sudo apt-get installe python3-pip"
  -pip3 install pyTelegramBotAPI
  
# Benutzung

Das Programm wird am besten über einen Cronjob periodisch aufgerufen, z.Bsp. Stündlich, immer zur halben Stunde, im Zeitraum von 7 bis 15 Uhr, an den Werk(Schul-)tagen Montag bis Freitag.
Eintrag in der crontab sollte dann in etwa so ausschauen (Pfad zum Script bitte anpassen):

30 7-15 * * 1-5 python3 /home/carsten/Scripts/mpgScanner.py

# Disclaimer

Diese Software benutz den Zugang zum Schulserver des Max-Planck-Gymnasiums in Ludwigshafen (http://www.mpglu.de/aktuelles/vertretungsplan.html), um dort die Vertretungspläne für den aktuellen und den darauf folgenden Schultag zu laden. Für die Feier- und Ferientagsdaten wird die API von smartnoob.de  (https://robin.meis.space/2014/04/15/ferien-feiertag-api-fuer-deutschland/) benutz. Vielen Dank für die Bereitstellung der Daten.

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.me/Hubobel)
