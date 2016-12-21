FROM alfpark/cntk:2.0beta4-gpu-openmpi

RUN sudo apt-get update
RUN sudo apt-get install -qq python-qt4
RUN sudo apt-get install -qq build-essential libssl-dev libffi-dev python-dev
RUN pip install Flask
RUN pip install azure-storage

COPY ./src /code
ADD entry.sh /code/
RUN chmod +x /code/entry.sh

EXPOSE 80
WORKDIR /code

ENTRYPOINT ["/code/entry.sh"]