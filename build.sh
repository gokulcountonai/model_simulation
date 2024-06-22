#!/bin/bash

zip -r Docker/main.zip * &&
sudo docker build -t countaiadmin/model-simulation Docker/ &&
sudo docker rm -f model-simulation &&
sudo docker run --restart=always -it --name model-simulation  -v /home/:/home/ -v /home/knit/projects/knit-i/weights:/app/uploads --network=host --privileged --log-opt max-size=200m --log-opt max-file=1 countaiadmin/model-simulation:latest