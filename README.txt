2022-01-28	
Neue Version ControlStream12.py

- Menueauswahl entfernt
- die FIFO-Pipe wird nun jeweisl ne erstellt (Start Stream) und wieder gelöscht (Stop Stream)
	Somit wird jeweil ein neuer Buffer ohne "alten" Inhalt bereitgestellt.
- die parameter vom OMX-Player könne nun testweise angepasst werden. Diese parameter werdne jeweis beim 
Start vom OMX player neun eingelesen: File:  /rins/shm/omxparms
Möglichkeiten: Sound auf HDMI oder auf Headphon ausgeben.
 
- Der Sound tönt noch immer blechik, keine abhilfe gefunden.
- Das Streamlog wird nun reverse ausgegeben, neues File streamlog.php
	File index.html angepasst.

- NGINX Server neu mit PHP, Konfiguration angepasst.
	neue Pakete  php und php-fpm


 
