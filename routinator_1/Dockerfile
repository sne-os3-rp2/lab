FROM dadepo/routinator-ipfs

WORKDIR /

COPY ./routinator.conf /home/routinator/.routinator.conf
COPY ./init_tal.sh /init_tal.sh
EXPOSE 9556

CMD ["server", "--http", "0.0.0.0:9556"]
#CMD ["server", "--rtr", "0.0.0.0:3323", "--http", "0.0.0.0:9556"]
