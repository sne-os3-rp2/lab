FROM dadepo/routinator-ipfs:v2

WORKDIR /

COPY ./routinator.conf /home/routinator/.routinator.conf
COPY ./init_tal.sh /init_tal.sh

USER 0
RUN apk add --no-cache sudo bash

RUN echo "routinator ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

USER 1012

EXPOSE 9556

ENTRYPOINT ["/init_tal.sh"]
CMD ["routinator", "server", "--http", "0.0.0.0:9556"]