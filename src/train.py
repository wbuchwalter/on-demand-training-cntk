import sys
import os

from cntk import Trainer, StreamConfiguration, text_format_minibatch_source, learning_rate_schedule, UnitType
from cntk.learner import sgd
from cntk.utils import get_train_eval_criterion, get_train_loss
from cntk.ops import *

import dataloader
import model
import hyperparameters as hp
import helper

dataloader.load()
train_file = "data/MNIST/Train-28x28_cntk_text.txt"

learning_rate = 0.2

if os.path.isfile(train_file):
    path = train_file
else:
    print("Cannot find data file")

feature_stream_name = 'features'
labels_stream_name = 'labels'

mb_source = text_format_minibatch_source(path, [
    StreamConfiguration(feature_stream_name, hp.input_dim),
    StreamConfiguration(labels_stream_name, hp.num_output_classes)])
features_si = mb_source[feature_stream_name]
labels_si = mb_source[labels_stream_name]

# Define a utility function to compute the moving average sum.
# A more efficient implementation is possible with np.cumsum() function
def moving_average(a, w=5):
    if len(a) < w:
        return a[:]    # Need to send a copy of the array
    return [val if idx < w else sum(a[(idx-w):idx])/w for idx, val in enumerate(a)]


# Defines a utility that prints the training progress
def print_training_progress(trainer, mb, frequency, verbose=1):
    training_loss = "NA"
    eval_error = "NA"

    if mb%frequency == 0:
        training_loss = get_train_loss(trainer)
        eval_error = get_train_eval_criterion(trainer)
        if verbose: 
            print ("Minibatch: {0}, Loss: {1:.4f}, Error: {2:.2f}%".format(mb, training_loss, eval_error*100))
        
    return mb, training_loss, eval_error

def save_metrics(trainer, filename):
    training_loss = get_train_loss(trainer)
    eval_error = get_train_eval_criterion(trainer)
    f = open(filename, 'w')
    f.write("Loss: {0:.4f}, Error: {1:.2f}%".format(training_loss, eval_error*100))

def get_trainer(model):

    input = input_variable((hp.input_dim), np.float32)
    label = input_variable((hp.num_output_classes), np.float32)
    
    #cost function
    loss = cross_entropy_with_softmax(model, label)

    #compute accuracy
    label_error = classification_error(model, label)

    # Instantiate the trainer object to drive the model training
    lr_schedule = learning_rate_schedule(learning_rate, UnitType.minibatch)
    learner = sgd(z.parameters, lr_schedule)
    return Trainer(z, loss, label_error, [learner])


def train(trainer):
    # Initialize the parameters for the trainer
    minibatch_size = 64
    num_samples_per_sweep = 60000
    num_sweeps_to_train_with = 10
    num_minibatches_to_train = (num_samples_per_sweep * num_sweeps_to_train_with) / minibatch_size

    # Run the trainer on and perform model training
    training_progress_output_freq = 500

    plotdata = {"batchsize":[], "loss":[], "error":[]}

    for i in range(0, int(num_minibatches_to_train)):
        mb = mb_source.next_minibatch(minibatch_size)
        
        # Specify the input variables mapping in the model to actual minibatch data to be trained
        arguments = {input: mb[features_si],
                    label: mb[labels_si]}
        trainer.train_minibatch(arguments)
        batchsize, loss, error = print_training_progress(trainer, i, training_progress_output_freq, verbose=1)
        
        if not (loss == "NA" or error =="NA"):
            plotdata["batchsize"].append(batchsize)
            plotdata["loss"].append(loss)
            plotdata["error"].append(error)

    trainer.save_checkpoint("../output/model")
    save_metrics(trainer, '../output/metrics.txt')
    helper.upload_results(sys.argv[1])

