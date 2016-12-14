#!/bin/bash

#dpkg is locked when the VM startups, se we have to wait a bit before executing our scrip
#see https://github.com/Azure/custom-script-extension-linux/issues/82 for more info.
sleep 5m

#Install NVIDIA driver and nvidia-docker that were pre-downloaded during our VM capture
apt-get install -qq linux-headers-`uname -r`
chmod +x /tools/NVIDIA-Linux-x86_64-375.20.run
sh /tools/NVIDIA-Linux-x86_64-375.20.run -a -s
dpkg -i /tools/nvidia-docker_1.0.0.rc.3-1_amd64.deb

#Get sources and build a docker image
cd /home/agent
git clone https://github.com/wbuchwalter/on-demand-training-vsts
cd on-demand-training-vsts

sudo docker build -f Dockerfile.train -t cntk-mnist .

#Run the training, the parameter we pass is coming from the ARM template and is the BuildId
sudo nvidia-docker run cntk-mnist $1
