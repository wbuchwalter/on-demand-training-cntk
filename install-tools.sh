#!/bin/bash
sudo apt-get install -qq linux-headers-`uname -r`
sudo chmod +x /tools/NVIDIA-Linux-x86_64-375.20.run
sudo sh /tools/NVIDIA-Linux-x86_64-375.20.run -a -s