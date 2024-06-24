#!/bin/bash

sudo curl -fsSL http://100.121.194.26/simulation/simulation.zip -o /home/kniti/projects/knit-i/simulation.zip &&
if [ -d /home/kniti/projects/knit-i/simulation ]; then
    sudo rm -rf /home/kniti/projects/knit-i/simulation
fi
sudo unzip /home/kniti/projects/knit-i/simulation.zip -d /home/kniti/projects/knit-i/ &&
sudo rm /home/kniti/projects/knit-i/simulation.zip &&
sudo docker login --username countaiadmin --password dckr_pat_YWuZvEphltmiGAjGYHQt36kL6Hg &&
sudo docker pull countaiadmin/simulation:latest &&
sudo docker pull countaiadmin/knitting-ml:latest &&
sudo docker logout &&
sudo docker rm -f model-simulation &&
echo "@reboot python3 /home/kniti/projects/knit-i/simulation/ml_restart.py" | sudo crontab -        
sudo docker run --restart=always -it --name model-simulation -v /home:/home -v /home/kniti/projects/knit-i/simulation:/app/simulation -v /home/kniti/projects/knit-i/simulation/output:/app/output -v /home/kniti/projects/knit-i/weights:/app/uploads --network=host --privileged --log-opt max-size=200m --log-opt max-file=1 countaiadmin/simulation:latest &&
sudo docker run --restart=always -it -v /home/kniti/projects/knit-i/weights:/app/weights --gpus all --network=host --privileged --log-opt max-size=500m --log-opt max-file=1 --device /dev/mem:/dev/mem --cap-add SYS_RAWIO    --name knitting-ml countaiadmin/knitting-ml:latest