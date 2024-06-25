#!/bin/bash

zip -r Docker/main.zip * &&
sudo docker build -t countaiadmin/simulation Docker/ &&
sudo docker rm -f model-simulation &&
sudo docker run --restart=always -it --name model-simulation -v /etc/localtime:/etc/localtime:ro -v /home:/home -v /home/kniti/projects/knit-i/simulation:/app/simulation -v /home/kniti/projects/knit-i/simulation/output:/app/output -v /home/kniti/projects/knit-i/weights:/app/uploads --network=host --privileged --log-opt max-size=200m --log-opt max-file=1 countaiadmin/simulation:latest
