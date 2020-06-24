#! /bin/bash

# run the parent init script

/opt/entrypoint.sh

sleep 5

wget --no-check-certificate https://192.168.1.101:3000/ta/ta.tal -O /home/routinator/.rpki-cache/tals/krill_1.tal
wget --no-check-certificate https://192.168.1.102:3000/ta/ta.tal -O /home/routinator/.rpki-cache/tals/krill_2.tal

exec "$@"





