FROM dadepo/krill-ipfs


WORKDIR /
COPY ./keys /data/ipfs/keystore/
COPY krill.conf /var/krill/data/
COPY ./data_generator.py /data_generator.py
RUN touch /var/krill/krill.log
RUN apk add python3
RUN apk add wget


CMD ["bash", "-c", "touch /tmp/lol ; krill -c /var/krill/data/krill.conf"]
# CMD ["krill", "-c", "/var/krill/data/krill.conf"]
