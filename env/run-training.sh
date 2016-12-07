#!/bin/bash
docker pull wbuchwalter/cntk-mnist:$1
nvidia-docker run --rm -v=/output:/code/output wbuchwalter/cntk-mnist:$1
