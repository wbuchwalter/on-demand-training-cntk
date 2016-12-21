import sys
import os

from cntk import StreamConfiguration, text_format_minibatch_source

import dataloader
import hyperparameters as hp
import helper
from model import Model

dataloader.load()
train_file = "data/MNIST/Train-28x28_cntk_text.txt"

if os.path.isfile(train_file):
    path = train_file
else:
    print("Cannot find data file")

feature_stream_name = 'features'
labels_stream_name = 'labels'

mb_source = text_format_minibatch_source(path, [
    StreamConfiguration(feature_stream_name, hp.input_dim),
    StreamConfiguration(labels_stream_name, hp.num_output_classes)])

model = Model()
model.train(mb_source)
model.save_metrics('../output/metrics.txt')
model.save_checkpoint('../output/model')
helper.upload_results(sys.argv[1])
