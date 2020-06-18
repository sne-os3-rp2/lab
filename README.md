## Lab

Dockerfile - Build image that can be used for experiments
Docker compose - Example of how the images can be used

## Instructions

To start up the services defined in the docker compose follow the following steps:

- Create /tmp/ipfs/nexus on your machine and grant read/write access #TODO confirm if this is actually necessary as docker compose should do this
- Clone this repository
- Make sure you are in the directory where `docker-compose.yml` file is located
- Then run the command `docker-compose up --build`. This builds the image and then run the container
- You can execute `docker exec -it krill_1 /bin/sh` to connect to `krill_1`
  - In `krill_1` there shuld be a `/data_generator.py` present. This is used to initialize the krill instance with both ca and roas
  - An example of how the `data_generator.py` script can be used is to run: `python3 data_generator.py --token itworks --host https://localhost:3000 --count 1 --roadepth 1 --sleeptime 1 -pr k1`
- You can execute `docker exec -it krill_2 /bin/sh` to connect to `krill_2`
  - In `krill_2` there shuld be a `/data_generator.py` present. This is used to initialize the krill instance with both ca and roas
  - An example of how the `data_generator.py` script can be used is to run: `python3 data_generator.py --token itworks --host https://localhost:3000 --count 1 --roadepth 1 --sleeptime 1 -pr k2`
- You can now execute `docker exec -u 0 -it routinator_1 /bin/sh to connect to `routinator_1`. Take note of the `-u 0` flag
  - In `routinator_1` there shuld be a `/init_tal.sh` present. This is used to downlaod the tal from the respective krill instances
  - Run `sh init_tal.sh 192.168.1.101` to download the tal from `krill_1`
  - Then exit the container and reconnect again.
  - Again run `sh init_tal.sh 192.168.1.102` to download the tal from `krill_2`
- No need to exit this time. Now execute `routinator -vvv vrps` Routinator should fetch roas using ipfs and validates

## TODO's
- Make it possible to also pass the file name to use to store the tal being download
- Remove the need to exit and connect again in between running executing `init_tal.sh`

