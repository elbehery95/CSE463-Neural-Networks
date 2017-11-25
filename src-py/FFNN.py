"""
Neural network layer class

Dependencies
-  Layer.py
    -  Numpy
    -  activation_functions.py
"""

from Layer import Layer
import activation_functions as actf
import numpy as np

class FFNN(object):
    """
    Implements a feed forward neural network with fully connected layers
    the training algorithm used is the error back-propagation with gradient descent

    ### args
    + layers_structure : a vector of ints that contain the number of neurons of each layer
    the number of ints represents the number of layers
    e.g. [input_layer, hidd_1, hidd2, ... hidd_n, out]

    ### attributes
    + layers : All the **hidden layers** and the **output layer**,
      the input layer is not included here instead the inputs are probed into the first hidden layer
    """

    def __init__(self, layers_structure, batch=1, eta=0.1, cost_funct='mse'):
        """
        Creates the layers, connectes them
        """
        #creates a chain of layers
        self.layers = [Layer(layers_structure[i], layers_structure[i-1], batch_size=batch, eta=eta)
                       for i in range(1, len(layers_structure))]
        # set the output layer cost function
        self.layers[-1].cost_funct = cost_funct
        if cost_funct == 'ce':
            self.layers[-1].f_act = actf.soft_max

    def probe_input(self, in_vect, debug=False):
        """
        Probes an input vector to the neural network
        and updates self.layers[i].output_vector
        """
        # probe the inputs at the input layer and update the 1st hidden layer output vector
        self.layers[0].fwd_pass(in_vect)

        # fwd pass all the inputs from pred. till the output layer
        for i in range(1, len(self.layers)):
            self.layers[i].fwd_pass(self.layers[i-1].out_vector)
        if debug:
            print "Output layer : \n", self.layers[-1].out_vector

    def err_bp(self, target_out_vect, debug=False):
        """
        Back propagates the error given the target values from the data-set

        ### args
        - target_out_vect : the target values for the output neurons
        """
        # calculate delta for all output neurons
        self.layers[-1].calc_delta_out(target_out_vect)

        for i in range(2, len(self.layers)+1):
            # back-propagate the error succ. layer by layer
            self.layers[-i].calc_delta_hidden(self.layers[-i+1])
    
        # All the delta terms are calculated, update weights
        for i in range(len(self.layers)):
            self.layers[i].update_weights()

        if debug:
            print "New weights @input layer: \n", np.sum(self.layers[0].weight_matrix)

    def train_step(self, in_vect, target_out_vect):
        """
        A single training step, accepts a batch of inputs or a single input

        ### args
        + in_vect : a col of inputs, a batch contains multiple cols
        + target_out_vect : desired output vector, a column of output. A batch contains multipl
        cols
        """
        self.probe_input(in_vect)
        self.err_bp(target_out_vect)
    
    def test_acc(self, input_vect, target_out_vect):
        """
        Returns the number of the correct classified items
        for the cifar-10 dataset. It supports batch calculation

        args:
        + input_vect : the neural network input to check
        + target_out_vect : the neural network desired output for the current input(s)

        returns:
        + ret : the amount of correct classified classes
        """
        self.probe_input(input_vect)
        #print "WTF: ", np.argmax(self.layers[-1].out_vector[:,5]), np.argmin(self.layers[-1].out_vector[:,5])
        #print "WTF: ", np.argmax(self.layers[-1].out_vector, axis=0), np.argmax(target_out_vect, axis=0)
        ret = np.sum(np.argmax(self.layers[-1].out_vector, axis=0) == np.argmax(target_out_vect, axis=0))
        #print ret
        return ret