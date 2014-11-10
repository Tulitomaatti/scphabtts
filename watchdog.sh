#!/usr/bin/env bash

PIDFILE="scphabtts.pid"

if [ -e "${PIDFILE}" ] && (ps -u $USER -f | grep "[ ]$(cat ${PIDFILE})[ ]"); then
  echo "scphabtts server is already running."
  exit 99
fi

screen "python main.py" & >> scphabtts.log &

echo $! > "${PIDFILE}"
chmod 644 "${PIDFILE}"
