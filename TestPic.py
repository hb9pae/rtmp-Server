
import pdb
import subprocess
import shlex 
import glob


pictures = "/home/pi/Testbild/*.JPG"


def playTestPict() :
	piclist = glob.glob(pictures)
	pics = ""
	for i in piclist:
		pics += str(i)+ " "

	cmd = "/usr/bin/fbi -t 5 --autozoom --noverbose --vt 1 "+ pics
	cmd1 = shlex.split(cmd)
	print("CMD: %s" % cmd1)
	subprocess.run(cmd1)
	#subprocess.run(shlex.split(cmd))
	#pdb.set_trace()


playTestPict()




