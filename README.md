## Lab

Dockerfile - Build image that can be used for experiments
Docker compose - Example of how the images can be used

## Instructions

### Running with IPFS
- create the number of routinators for the test by running `./ipfs/scripts/create_docker_compose.py -c2` where `-c` is used to specify number of routinators to be created
- Run the only the krill instance and populate it with content
  - start only the krill instance by running `./ipfs/docker-compose up -d --build krill_1`
  - populate the krill instance by running `./ipfs/scripts/init_krills.py -co 1 -rd 1` where `co` is the number of child cas to be created and `rd` is how many times to divide the slash 24 that would be used for roa creation. Max `rd` is 8
  - TODO make it (or check) that the generated data can be shared instead of reran
- Start the script that would be used to collect data by running `./shared/result_fetcher.py -c 2 -d 200` where `-c` specifies the number of routinators running and `-d` specifies how long in seconds to poll for results (note by default validation takes place every 60 seconds)
- Now start the routinators instances. Do this by running `./ipfs/docker-compose up --build` you can include `-d` to detach. This command will start all the other containers that were not started when the krill instance was started.
- Check output.csv for results. TODO append timestamp and type to file name as we did with the raw benchmark

### Running with RRDP
- create the number of routinators for the test by running `./rrdp/scripts/create_docker_compose.py -c2` where `-c` is used to specify number of routinators to be created
- Run the only the krill instance and populate it with content
  - start only the krill instance by running `./rrdp/docker-compose up -d --build krill_unmodified_1`
  - populate the krill instance by running `./rrdp/scripts/init_krills.py -co 1 -rd 1` where `co` is the number of child cas to be created and `rd` is how many times to divide the slash 24 that would be used for roa creation. Max `rd` is 8
  - TODO make it (or check) that the generated data can be shared instead of reran
- Start the script that would be used to collect data by running `./shared/result_fetcher.py -c 2 -d 200` where `-c` specifies the number of routinators running and `-d` specifies how long in seconds to poll for results (note by default validation takes place every 60 seconds)
- Now start the routinators instances. Do this by running `./rrdp/docker-compose up --build` you can include `-d` to detach. This command will start all the other containers that were not started when the krill instance was started.
- Check output.csv for results. TODO append timestamp and type to file name as we did with the raw benchmark



