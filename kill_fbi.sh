# zuerst alle PIDs suchen und in einer
# Shell-Variablen speichern:
PIDS=$(ps -C fbi -o pid=)
   
# falls gefunden (fbi laeuft noch) killen:
if [ -n "$PIDS" ]
  then
  # Signal senden: bitte beenden
  kill -HUP $PIDS > /dev/null 2>&1
  sleep 3
  # fuer hartnaeckige Faelle
  kill -9 $PIDS > /dev/null 2>&1
  fi
  echo "done...."
# hier fbi neu starten
