from flask import Flask
import json
from cntk.ops import *

from model import Model
import helper

app = Flask(__name__)
model = Model()

# TODO: route with image data passed as post
# @app.route("/classify/<data>")
# def predict(data):
#     predictions = model.predict(data)
#     print(predictions)
#     return predictions.toJson()

#TODO: Grab the latest checkpoint
buildId = 99
helper.download_checkpoint_file(buildId)
model.restore_from_checkpoint(checkpoint_file_name)

if __name__ == "__main__":
    app.run(host= '0.0.0.0', port=80)

