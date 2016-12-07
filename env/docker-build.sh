#!/bin/bash
git clone https://github.com/wbuchwalter/on-demand-training-vsts
cd on-demand-training-vsts/src
docker build -t cntk-mnist .
