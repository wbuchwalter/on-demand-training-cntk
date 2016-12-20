import cntk
from cntk.initializer import glorot_uniform
from cntk.ops import *

import hyperparameters as hp


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

def get(input):
    # Scale the input to 0-1 range by dividing each pixel by 256.
    scaled_input = element_times(constant(1.0 / 256.0), input)
    # Create the fully connected classifier.
    z = fully_connected_classifier_net(scaled_input, hp.num_output_classes, hp.hidden_layers_dim, hp.num_hidden_layers, relu)
    return z

def predict(model, inputData):
    input = input_variable((hp.input_dim), np.float32)
    prediction = model.eval({input: inputData})
    return prediction

    