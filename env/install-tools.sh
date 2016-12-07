#!/bin/bash
sudo apt-get install -qq linux-headers-`uname -r`
sudo chmod +x /tools/NVIDIA-Linux-x86_64-375.20.run
sudo sh /tools/NVIDIA-Linux-x86_64-375.20.run -a -s
sudo dpkg -i /tools/nvidia-docker_1.0.0.rc.3-1_amd64.deb