FROM alfpark/cntk:2.0beta4-gpu-openmpi
RUN sudo apt-get update
RUN sudo apt-get install -qq python-qt4
COPY . /code

CMD ["python","/code/main.py"]