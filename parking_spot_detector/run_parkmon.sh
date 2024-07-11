#!/bin/bash

cd /home/pi/parkmon

LOGFILE="run_parkmon.log"

source pm_env/bin/activate
source .env_secrets

while true; do

  python3 app.py >> $LOGFILE 2>&1
  EXIT_CODE=$?

  if [ $EXIT_CODE -eq 0 ]; then
    echo "Exiting..."
    break
  else
    echo "Restarting parkmon..." >> $LOGFILE
    sleep 10
  fi
done
