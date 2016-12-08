#!/bin/bash

#Install Driver and nvidia-docker
sudo apt-get install -qq linux-headers-`uname -r`
sudo chmod +x /tools/NVIDIA-Linux-x86_64-375.20.run
sudo sh /tools/NVIDIA-Linux-x86_64-375.20.run -a -s
sudo dpkg -i /tools/nvidia-docker_1.0.0.rc.3-1_amd64.deb

#Get sources and build a docker image
cd /home/agent
sudo git clone https://github.com/wbuchwalter/on-demand-training-vsts
cd on-demand-training-vsts/src
sudo docker build -t cntk-mnist .

#Run the training, with a volume to save output
sudo nvidia-docker run --rm -v=/home/agent/output:/code/output cntk-mnist