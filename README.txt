README.txt
----------

Funktion
Wir detektieren pulizierte Streams unter /run/shm/ngin und spielen den ersten gefundenen Stream ab.


2022-10-16; 
Version 16
	Testbilder  sind nun im Verzeichnis /home/pi/Testbild
	Upgrade Libs
	Wir generien zwei PTT Signale:  
	- GPIO 23  Pin 16  geht HIGH
	- GPIO 21 Pin 40 geth LOW


2022-02-12: Mehrere Testbilder 
Version 15;
	im Verzeichnis /home/pi/Testbild/ können nun verschidenen Testbilder hinterlegt werden
	Format/Bewzeichnung  *.JPG (Suffix "JPG" in Grossbuchstaben


2022-02-04:Erweiterung derVersion 

Version 14
	Versionstring beim Init() ausgeben
	Soundausgabe lokal & HDMI
	Soundkarten HDMI und Headphone werden auf 0%  Volume und muted
	PTT Signalisation,  
	- GPIO23 RPI-Pin 16 geht auf HIGH
	- GPIO21 RPI-Pin 40 geht auf LOW


Version 13
- TestPlaer eingebaut, Steuerung mit Streamschlüssel.
Der Streamschlüssel definiert die Aktion und der verwendete Audio-Ausgang
Streamschlussel = 
	1	Speaker Test  HDMI
	2	Speaker Test  Headphone
	3	Abspielen MP4 Video HDMI 
	4	Abspielen MP4 Video Headphone 

2022-01-28:	hb9pae:	neue Version
	Variabler Parameter für  OMX-Player, PArameter unter /run/shm/pmxcmd werden beim Start OMX-Plaer gelesen
	Menue Auswahl entfernt
	FIFO-Pipe wird vor dem Streamen neu erstellt, nach dem Streamen geloescht

"""



Version 16
Diese hat zwei PTT-Signale, diese werden beim Abspielen eines Streams 
aktiv: 

- GPIO 23  Pin 16  geht HIGH
- GPIO 21  Pin 40 geht LOW

+ 5V findest auf Pin 2 und 4
GND findest auf Pin 4

PTT: Die GPIO's können keine Relais direkt treiben, dazu eine Transistor, FET
oder einen Optokoppler einsetzen.
-------------------

2022-01-28	
Neue Version ControlStream12.py

- Menueauswahl entfernt
- die FIFO-Pipe wird nun jeweisl neu erstellt (Start Stream) und wieder gelöscht (Stop Stream)
	Somit wird jeweil ein neuer Buffer ohne "alten" Inhalt bereitgestellt.

- die Parameter vom OMX-Player könne nun testweise angepasst werden. Diese Parameter werden jeweis beim 
Start vom OMX Player neu eingelesen: File:  /rins/shm/omxparms
Möglichkeiten: Sound auf HDMI oder auf Headphon ausgeben.
 
- Der Sound tönt noch immer blechig, keine Abhilfe gefunden.
- Das Streamlog wird nun reverse ausgegeben, neues File streamlog.php
	File index.html angepasst.

- NGINX Server neu mit PHP, Konfiguration angepasst.
	neue Pakete  php und php-fpm


Hilfsprogramme
https://www.codegrepper.com/code-examples/python/python+check+if+a+program+is+running
#Iterates through all the programs running in your system and checks for the one in the string

import psutil    
"someProgram" in (p.name() for p in psutil.process_iter())
#https://pymotw.com/2/multiprocessing/basics.html


 
