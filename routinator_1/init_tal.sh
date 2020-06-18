#! /bin/sh

function fetch_tal()
{
tal_url="https://$1:3000/ta/ta.tal"

wget --no-check-certificate $tal_url -P /home/routinator/.rpki-cache/tals/

echo $tal_url
}


passed_in_url=$1

if ["" == "$passed_in_url"]
then
   echo "Pass in the url to fetch the tal from"
else
  fetch_tal $passed_in_url

fi

su routinator