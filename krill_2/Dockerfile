FROM krill-ipfs


WORKDIR /
COPY ./keys /data/ipfs/keystore/
COPY krill.conf /var/krill/data/
COPY ./data_generator.py /data_generator.py
RUN apk add python3
RUN apk add wget
RUN touch /var/krill/krill.log
EXPOSE 3000
EXPOSE 3001
EXPOSE 4001 
EXPOSE 8080
EXPOSE 8081
EXPOSE 5001


CMD ["bash", "-c", "touch /tmp/lol ; krill -c /var/krill/data/krill.conf"]
# CMD ["krill", "-c", "/var/krill/data/krill.conf"]
