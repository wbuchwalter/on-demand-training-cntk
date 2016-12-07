import cntk
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import sys
import os

from cntk import Trainer, StreamConfiguration, text_format_minibatch_source, learning_rate_schedule, UnitType
from cntk.initializer import glorot_uniform
from cntk.learner import sgd
from cntk.ops import *
from cntk.utils import get_train_eval_criterion, get_train_loss

image_size = 28
input_dim = image_size * image_size
num_output_classes = 10
num_hidden_layers = 2
hidden_layers_dim = 400

train_file = "data/MNIST/Train-28x28_cntk_text.txt"

if os.path.isfile(train_file):
    path = train_file
else:
    print("Cannot find data file")

feature_stream_name = 'features'
labels_stream_name = 'labels'

mb_source = text_format_minibatch_source(path, [
    StreamConfiguration(feature_stream_name, input_dim),
    StreamConfiguration(labels_stream_name, num_output_classes)])
features_si = mb_source[feature_stream_name]
labels_si = mb_source[labels_stream_name]

input = input_variable((input_dim), np.float32)
label = input_variable((num_output_classes), np.float32)

# Define a fully connected feedforward network

def linear_layer(input_var, output_dim):

    input_dim = input_var.shape[0]
    times_param = parameter(shape=(input_dim, output_dim), init=glorot_uniform())
    bias_param = parameter(shape=(output_dim))

    t = times(input_var, times_param)
    return bias_param + t

def dense_layer(input, output_dim, nonlinearity):
    r = linear_layer(input, output_dim)
    r = nonlinearity(r)
    return r

def fully_connected_classifier_net(input, num_output_classes, hidden_layer_dim, 
                                   num_hidden_layers, nonlinearity):
    
    h = dense_layer(input, hidden_layer_dim, nonlinearity)
    for i in range(1, num_hidden_layers):
        h = dense_layer(h, hidden_layer_dim, nonlinearity)
    r = linear_layer(h, num_output_classes)
    return r


# Scale the input to 0-1 range by dividing each pixel by 256.
scaled_input = element_times(constant(1.0 / 256.0), input)
# Create the fully connected classifier.
z = fully_connected_classifier_net(scaled_input, num_output_classes, hidden_layers_dim, num_hidden_layers, relu)

print(label)

#cost function
loss = cross_entropy_with_softmax(z, label)

#compute accuracy
label_error = classification_error(z, label)

# Instantiate the trainer object to drive the model training
learning_rate = 0.2
lr_schedule = learning_rate_schedule(learning_rate, UnitType.minibatch)
learner = sgd(z.parameters, lr_schedule)
trainer = Trainer(z, loss, label_error, [learner])


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