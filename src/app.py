from flask import Flask
import json
from cntk.ops import *

import model
import train
import helper

app = Flask(__name__)
model = model.get()


# TODO: route with image data passed as post
# @app.route("/classify/<data>")
# def predict(data):
#     predictions = model.predict(model, data)
#     #import weight
#     print(predictions)
#     return predictions.toJson()

#TODO: Grab the latest checkpoint
buildId = 99
helper.download_checkpoint_file(buildId)
trainer = train.get_trainer(model)
trainer.restore_from_checkpoint(checkpoint_file_name)

if __name__ == "__main__":
    app.run(host= '0.0.0.0', port=80)

