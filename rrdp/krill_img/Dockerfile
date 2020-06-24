FROM nlnetlabs/krill:v0.6.2


WORKDIR /

COPY ./data_generator.py /data_generator.py

RUN apk add python3
RUN apk add wget
RUN apk add iproute2

CMD ["bash", "-c", "krill -c /var/krill/data/krill.conf"]
