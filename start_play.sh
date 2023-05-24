
FIFO="/tmp/rtmp-pipe"

if test -f  "$FIFO"; then
	mkfifo /tmp/rtmp-pipe
fi

/usr/bin/rtmpdump -v -r "rtmp://localhost/live/$1" -o $FIFO > /dev/null 2>&1 & 
/usr/bin/omxplayer -p -o hdmi $FIFO > /dev/null 2>&1  &

