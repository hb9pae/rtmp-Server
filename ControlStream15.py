#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import os 
import os.path
import time
import subprocess
import pdb
import datetime
import shlex
import multiprocessing
import RPi.GPIO as GPIO
import glob


""" 
Wir detektieren pulizierte Streams unter /run/shm/ngin und spielen den ersten gefundenen
Stream ab.
https://www.codegrepper.com/code-examples/python/python+check+if+a+program+is+running
#Iterates through all the programs running in your system and checks for the one in the string
import psutil    
"someProgram" in (p.name() for p in psutil.process_iter())
#https://pymotw.com/2/multiprocessing/basics.html


2022-02-12: Mehrere Testbilder 
Version 15;
	im Verzeichnis /home/pi/Testbild/ können nun verschidenen Testbilder hinterlegt werden
	Format/Bewzeichnung  *.JPG (Suffix "JPG" in Grossbuchstaben


2022-02-04:Erweiterung derVersion 

Version 14
	Versionstring beim Init() ausgeben
	Soundausgabe lokal & HDMI
	Soundkarten HDMI und Headphone werden auf 0%  Volume und muted
	PTT Signalisation,  GPIO23 RPI-Pin 16

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



version = "V 15"
omxcmd="/run/shm/omxcmd"
audiodevice = "both"

streamlistpath = "/run/shm/nginx/"
logfile = "/var/www/stream.log"
pictures = "/home/pi/Testbild/*.JPG"
activestream = ""
testbild = False
debug = True
fifo = '/tmp/rtmp_fifo'

pttPin = 23  # PI pin 16

def ptt(state) :
	GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
	GPIO.setup(pttPin, GPIO.OUT) # PTT pin set as output
	if (state) :
		GPIO.output(pttPin, GPIO.HIGH)
	else :
		GPIO.output(pttPin, GPIO.LOW)

	logActivity("Set PTT %s" % state)

def muteSounds() :

	cmd = "sudo amixer -c0 sset HDMI 0%, 0%"
	subprocess.run(shlex.split(cmd))
	cmd = "sudo amixer -c1 sset Headphone 0%, 0%"
	subprocess.run(shlex.split(cmd))
	cmd = "sudo amixer -c0 sset HDMI mute"
	subprocess.run(shlex.split(cmd))
	cmd = "sudo amixer -c1 sset Headphone mute"
	subprocess.run(shlex.split(cmd))
	logActivity("Mute Alsamixer HDMI & Headphone now" )

def unmuteSounds() :
	cmd = "sudo amixer -c0 sset HDMI 80%, 80%"
	subprocess.run(shlex.split(cmd))
	cmd = "sudo amixer -c1 sset Headphone 80%, 80%"
	subprocess.run(shlex.split(cmd))
	cmd = "sudo amixer -c0 sset HDMI unmute"
	subprocess.run(shlex.split(cmd))
	cmd = "sudo amixer -c1 sset Headphone unmute"
	subprocess.run(shlex.split(cmd))
	logActivity("Unmute Alsamixer HDMI & Headphone now" )


def setOMXParams() :
	f = open(omxcmd, "w")
	params = " -I -o %s " % (audiodevice)
	f.write(params)
	f.close

def getOMXParams() :
	if os.path.exists(omxcmd) :
		f = open(omxcmd, "r")
		cmd = f.read() 
	return(cmd)

def playTestPict() :
	global testbild
	piclist = glob.glob(pictures)
	pics = ""
	for i in piclist:
		pics += str(i)+ " "

	cmd = "/usr/bin/fbi -t 30 --autozoom --noverbose --vt 1 " + pics
	subprocess.run(shlex.split(cmd))
	print("CMD: %s" % cmd)
	#pdb.set_trace()
	testbild = True
	ptt(False)
	logActivity("Start play Testpicture %s now" % piclist)
	logActivity("-----------")

def stopTestPict() :
	global testbild
	cmd = "sudo fbi -t 1 -1 --vt 1 "  + pictures  
	subprocess.run(shlex.split(cmd))
	testbild = False
	cmd = "sudo killall fbi"
	subprocess.run(shlex.split(cmd))
	logActivity("Stop play Testpicture %s now" % pictures)

def playStream(name) :
	global activestream
	activestream = name
	rtmp = multiprocessing.Process(target=rtmpDump)
	rtmp.start()
	logActivity("Start RTMP-Dump Stream %s" % (activestream)  )
	time.sleep(1)

	omx = multiprocessing.Process(target=omxplayer)
	#pdb.set_trace()
	ptt(True)
	omx.start()
	logActivity("Start OMX-Player Stream" )
	time.sleep(1)

def rtmpDump() :
	global activestream
	if not os.path.exists(fifo) :
		mode = 0x644
		os.mkfifo(fifo, mode)
		logActivity("make FIFO-Pipe %s " % fifo)
	cmd = "/usr/bin/rtmpdump -v -r rtmp://localhost/live/"+ activestream + " -o " + fifo 
	subprocess.run(shlex.split(cmd))

def killrtmpDump() :
	#cmd = "/usr/bin/killall /usr/bin/rtmpdump"
	cmd = "/usr/bin/killall rtmpdump"
	subprocess.run(shlex.split(cmd))
	logActivity("Kill RTMP-Dump" )
	if os.path.exists(fifo) :
		os.remove(fifo)
		logActivity("Kill FIFO" )

def omxplayer() :
	#pdb.set_trace()
	if not os.path.exists(fifo) :
		logActivity("Error: no Pipe found %s" % fifo )
		return(1)
	param = getOMXParams()
	cmd = "/usr/bin/omxplayer " + param + fifo
	logActivity("OMX-Player parameter %s" % (cmd) )
	subprocess.run(shlex.split(cmd))

def killOMXplayer() :
	#cmd = "/usr/bin/killall /usr/bin/omxplayer"
	cmd = "/usr/bin/killall omxplayer"
	subprocess.run(shlex.split(cmd))
	cmd = "/usr/bin/killall omxplayer.bin"
	subprocess.run(shlex.split(cmd))
	logActivity("Kill OMX-Player" )

def logActivity(logtext) :
	now = datetime.datetime.now()
	log = now.strftime("%Y-%m-%d %H:%M:%S ") + logtext + "\n"
	if debug :
		print(log)
	with open(logfile, "a") as f :
		f.write(log)
 
def chkProcessList() :
	# check if  this script already running
	cmd = 'pgrep -f ' + sys.argv[0]
	process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	my_pid, err = process.communicate()
	#pdb.set_trace()
	num = my_pid.splitlines()
	if len(num) > 2 :
		return(True)
	else :
		return(False)

def playTest(name) :
	global activestream
	global audiodevice

	activestream = name
	unmuteSounds()
	cmdlist = []  
	cmdlist.append("/usr/bin/speaker-test -D hw:0 -t wav -c 2 -l 3")
	cmdlist.append("/usr/bin/speaker-test -D hw:1 -t wav -c 2 -l 3")
	cmdlist.append("/usr/bin/omxplayer -o hdmi /home/pi/MP4/bbb_sunflower_1080p_60fps_normal.mp4" )
	cmdlist.append("/usr/bin/omxplayer -o local /home/pi/MP4/bbb_sunflower_1080p_60fps_normal.mp4" )
	cmd = cmdlist[((int(name)-1)  % len(cmdlist))]
	logActivity("Start Soundtest SoundCard 0: %s" % (cmd) )
	subprocess.run(shlex.split(cmd))
	logActivity("Stop Soundtest %s" % (cmd) )
	time.sleep(5)
	muteSounds()
	activestream = ""

def getStreamList() :
	return(os.listdir(streamlistpath))

def init():
	logActivity("Init %s" % (version))
	stopTestPict()
	killrtmpDump()
	killOMXplayer()
	muteSounds()
	ptt(False) 

def initStream(name) :
	cmd = "sudo touch /run/shm/nginx/" + name
	subprocess.run(shlex.split(cmd))
	logActivity("Init Stream %s" % name)

def autorun() :
	global activestream
	setOMXParams()

	while 1 :
		#pdb.set_trace()
		Streams=getStreamList()
		if (len(Streams) > 0) :
			if testbild :
				stopTestPict()	
			if (Streams[0].isnumeric() ) :
				playTest(Streams[0]) 

			else :
				playStream(Streams[0])
				while 1:
					time.sleep(5)
					Streams=getStreamList()
					if (len(Streams) < 1) or (Streams[0] != activestream) :
						logActivity("Closed Stream %s" % activestream)
						killrtmpDump()
						killOMXplayer()
						activestream = ""
						break
		else :
			if not testbild :
				playTestPict()
			else :
				time.sleep(5)




# ---- main() -------
def main() :
	logActivity("Autorun")
	autorun()

if __name__ == '__main__':
        init()
        main()

