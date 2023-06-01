#   RTMP-Server 
Version 17, 2023-05-30, hb9pae

---
##	Server Status
	[title](https://www.example.com)

-	[RTMP-Server Status](stats.xls)
-	ÇRTMP-Server Logfile](streamlog.php)
---
##	Video-Streams
Mit dem VLC-Player könen folgende Video-Streams abgerufen werden

-	Flash Video:	rtmp://«IP-ADRESSE>/vod/sample.flv
-	MP4 Video 1		rtmp://«IP-ADRESSE»/vod2/1.mp4
-	MP4 Video 2		rtmp://«IP-ADRESSE»/vod2/2.mp4
-	MP4 Video 3		rtmp://«IP-ADRESSE»/vod2/3.mp4
-	MP4 Video 4		rtmp://«IP-ADRESSE»/vod2/4.mp4
---

#	Kurzbeschreibung
Dieses Programmpaket steuert ein digitales Amteurfunk-TV Relais (DATV) mit 
einen DATV Umsetzer. 

##  Einleitung
Funkamateure senden ihre ATV-Signale über Internet zum Umsetzer, dieser empfängt die Signale 
und sendet Bild- und Tondaten auf einer Amateurfunkfrequenz wieder aus.
Gleichzeitig verteilt der RTPM-Server die empfangenen Streamdaten über seine Internet-
adressen wieder an weitere Empfänger. Ab der Version 17 läuft das Programm auf einem Raspberry 
PI Model 4, das Modell 3+ wird nicht mehr unterstützet. 

##  Funktionsbeschreibung
Der RTMP-Server wartet auf einen RTMP-Datenstream (Video und Audio). Wird eine gültiger 
Datenstream resp. Streamschlüsssel erkannt,  wird die PTT aktiviert und der Datenstream
(Video & Audio) auf dem HDMI-Anschluss ausgegeben. 
Parallel wird der Datenstream zum Download über die eigene Ethernet-Schnittstelle ausgegeben.
Das Audio-Signal wird zusätzlich noch auf der Soundkarte ausgegeben.
Im Idle-Mode (kein RTMP-Datenstream) werden auf der HDMI-Schnittstelle Testbilder ausgegeben. 
 
##  Programm-Komponenten
Zur Steuerung dient eine Python Programm, das je nach Status die einzelnen Subprozesse 
startet oder stopt.

1.  RTMP-Server
Als RTMP-Server dient der NGINX-Webserver mit dem Zusatzmodul "nginx-rtmp-module"
Erkennt der RTMP-Server gültige Stream-Daten schreibt er den Streamschlüssel unter 
/run/shm/nginx. Der RTMP-Server stellt die Streamdaten unter 
rtmp://localhost/live/STREAMSCHLUESSEL zur Verfügung. 

2. IDLE-MODE
Bedingung: Streamschlüssel (/run/shm/nginx) nicht vorhanden.
Ausgabe der Testbiler aus dem Verzeichnis "Testbilder" an die HDMI-Schnittstelle
Intervall 30 Sekunden. Format: JPG ode PNG. Filename beliebig, Suffix ".JPG" 
Process: playTestPict, fbi - Linux framebuffer imageviewer 

3. RTMP-Mode 
Bedingung: Streamschlüssel (String, normalerweise Rufzeichen des Funkamteurs)
Wird ein Streamschlüssel erkannt, beendet die Logik den IDLE-Mode und wechselt in den RTMP-Mode. 
Die vom RTMP-Server empfangenen Stream-Daten werden in einen FIFO-Buffer geschrieben. 
Process:  rtmpdump - toolkit for RTMP streams
Der Process OMX-Player liest die Daten aus dem FIFO-Buffer aus und sendet diese Stream-
Daten an die HDMI Schnittstelle.

4.  RTMP-Test MODE
Bedingung: Streamschlüssel numerisch  1, 2, 3 oder 4

Test Mode:
	1:	Playback device 0 Speaker Test stereo
	2:	Playback device 1 Speaker Test stereo

	3:	Playback MP4 Video 1080p 60fps über HDMI
	4:	Playback MP4 Video 1080p 60fps local
	

##   Logfile
Star- / Stop der Betriebsmodes oder Fehlermeldungen werden in das Logfile geschrieben.
LOG:  /var/www/stream.log  oder http://<IP>/streamlog.php

##   Streamstatus
Der Streemastatus ist unter http://<IP>/stats.xls verfügbar. 

##   Betrieb
Das Programm läuft im Hintergrund und wird durch den Systemdienst systemd aufgerufen:
sudo systemctl enable controlstream			Autostart erlauben
Mit einem Reboot wird das Programm automatisch gestartet.  
 
##  Publizieren mit OBS Studio 
Zum Publizieren des DATV-Datenstreams kann OBS (Open Broadcast Studio) verwendet werden.
Konfiguration OBS:	Neben der Serveradresse  (rtmp://10.10.10.1/live) muss auch das eigene 
Rufzeichen als Streamschlüssel eingetragen werden. 

##  DATV-Stream empfangen (VLC Player)
Mit dem VLC Player kann der aktuelle Datenstream empfangen und angezeigt werden.

##  Test Modes
Folgende Test modes stehen zur Verfügung. Die Selektion der Test erfolgt mit dem OBS Streamschlussel:

- Streamschlüssel = 1 	AUDIO-TEST via HDMI und der eingbauten Soundkarte (Device hw:0)
- Streamschlüssel = 2 	AUDIO-TEST via externe USB-Soundkarte (Device hw:1)
 
- Streamschlüssel = 3		Abspielen eines MP4 Videos über HDMI bbb_sunflower_1080p_60fps_normal.mp4"   
- Streamschlüssel = 4		Abspielen eines MP4 Videos über den lokalen Videoausgang bbb_sunflower_1080p_60fps_normal.mp4"   

- Abruf Video mit VLC
Anstelle des Live-Streams können mit VLC folgende Videosequenzen abgerufen werden:

	- rtmp://<IP-ADRESSE>vod/sample.flv		Play Flash Video
	- rtmp://<IP-ADRESSE>/vod2/1.mp4			Play MP4 Video 1	
	- rtmp://<IP-ADRESSE>/vod2/2.mp4			Play MP4 Video 2	
	- rtmp://<IP-ADRESSE>/vod2/3.mp4			Play MP4 Video 3	
	- rtmp://<IP-ADRESSE>/vod2/4.mp4			Play MP4 Video 4	

## Referenzen
fbi: https://manpages.ubuntu.com/manpages/bionic/man1/fbi.1.html
rtmpdump:	https://rtmpdump.mplayerhq.hu/
OBS:	https://obsproject.com/

