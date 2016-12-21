import hyperparameters as hp
from cntk import *
from cntk.layers import *
from cntk.ops import *
from cntk.learner import sgd
from cntk.utils import get_train_eval_criterion, get_train_loss
from cntk.initializer import glorot_uniform

class Model:
    def __init__(self):
        self.model, self.trainer, self.loss = self._create()
    
    def _create(self):
        feature = input_variable((hp.input_dim), np.float32)
        label = input_variable((hp.num_output_classes), np.float32)

        w1 = parameter(shape=(hp.input_dim, hp.hidden_layer_size), init=glorot_uniform())
        b1 = parameter(shape=(hp.hidden_layer_size))
        h1 = relu(times(feature, w1) + b1)

        w2 = parameter(shape=(hp.hidden_layer_size, hp.num_output_classes), init=glorot_uniform())
        b2 = parameter(shape=(hp.num_output_classes))
        h2 = times(h1, w2) + b2

        self.model = h2
        
        loss = cross_entropy_with_softmax(model, label)
        label_error = classification_error(model, label)

        lr_schedule = learning_rate_schedule(hp.learning_rate, UnitType.minibatch)
        learner = sgd(model.parameters, lr_schedule)

        return self.model, Trainer(model, loss, label_error, [learner]), loss
    
    def predict(self, s):
        return self.model.eval(s)

    def train(self, mb_source):
        # Initialize the parameters for the trainer
        minibatch_size = 64
        num_samples_per_sweep = 60000
        num_sweeps_to_train_with = 10
        num_minibatches_to_train = (num_samples_per_sweep * num_sweeps_to_train_with) / minibatch_size

        # Run the trainer on and perform model training
        training_progress_output_freq = 500

        plotdata = {"batchsize":[], "loss":[], "error":[]}

        feature_stream_name = 'features'
        labels_stream_name = 'labels'
        features_si = mb_source[feature_stream_name]
        labels_si = mb_source[labels_stream_name]

        for i in range(0, int(num_minibatches_to_train)):
            mb = mb_source.next_minibatch(minibatch_size)
            
            # Specify the input variables mapping in the model to actual minibatch data to be trained
            arguments = dict(zip(self.loss.arguments, [mb[features_si], mb[labels_si]]))
            
            self.trainer.train_minibatch(arguments)
            batchsize, loss, error = self.print_training_progress(i, training_progress_output_freq)
            
            if not (loss == "NA" or error =="NA"):
                plotdata["batchsize"].append(batchsize)
                plotdata["loss"].append(loss)
                plotdata["error"].append(error)

    def print_training_progress(self, idx, frequency, verbose=1):
        training_loss = "NA"
        eval_error = "NA"

        if idx%frequency == 0:
            training_loss = get_train_loss(self.trainer)
            eval_error = get_train_eval_criterion(self.trainer)
            if verbose: 
                print ("Minibatch: {0}, Loss: {1:.4f}, Error: {2:.2f}%".format(idx, training_loss, eval_error*100))
            
        return idx, training_loss, eval_error
    
    def save_metrics(self, filename):
        dir = os.path.dirname(filename)
        if not os.path.exists(dir):
            os.makedirs(dir)

        training_loss = get_train_loss(self.trainer)
        eval_error = get_train_eval_criterion(self.trainer)
        f = open(filename, 'w')
        f.write("Loss: {0:.4f}, Error: {1:.2f}%".format(training_loss, eval_error*100))

    def save_checkpoint(self, filename):
        self.trainer.save_checkpoint(filename)