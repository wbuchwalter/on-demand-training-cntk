#!/bin/bash
if [[ $1 == 'train' ]]; then
  python /code/train.py $2
else 
  python /code/app.py
fi