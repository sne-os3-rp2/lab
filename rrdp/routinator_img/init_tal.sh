#! /bin/bash

sleep 5

wget --no-check-certificate https://192.168.2.101:3000/ta/ta.tal -O /home/routinator/.rpki-cache/tals/krill_unmodified_1.tal

sed -i "1s~.*~https://krill1:3000/ta/ta.cer~" "/home/routinator/.rpki-cache/tals/krill_unmodified_1.tal"

exec "$@"





