#!/bin/bash
echo $1
python /code/main.py
python /code/upload-result.py $1
