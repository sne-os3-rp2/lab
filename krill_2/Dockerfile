FROM dadepo/krill-ipfs


WORKDIR /
COPY ./keys /data/ipfs/keystore/
COPY krill.conf /var/krill/data/
COPY ./data_generator.py /data_generator.py
RUN apk add python3
RUN apk add wget
RUN touch /var/krill/krill.log

CMD ["bash", "-c", "krill -c /var/krill/data/krill.conf"]
