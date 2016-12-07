#!/bin/bash
#docker pull wbuchwalter/cntk-mnist:$1
#nvidia-docker run --rm -v=/output:/code/output wbuchwalter/cntk-mnist:$1
git clone https://github.com/wbuchwalter/on-demand-training-vsts
cd on-demand-training-vsts/src
docker build -t cntk-mnist .
nvidia-docker run --rm -v=/output:/code/output cntk-mnist
