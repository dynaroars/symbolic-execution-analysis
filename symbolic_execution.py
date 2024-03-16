from keras.models import Sequential
from keras.layers import Dense
from keras import activations
import tensorflow as tf
import random

def get_info(layer: Dense):
    """
    Extract weights and bias from a layer
    """
    weights = layer.kernel_initializer.value
    bias = layer.bias_initializer.value
    return (weights, bias)

def generate_symbolic_execution(dnn: Sequential, library):
    """
    Return symbolic states from a dnn following the format of given library
    Args:
        dnn (type: Sequential)
        library (e.g. z3, cvc5)
    """
    constraint_list = []
    layers = dnn.layers

    # Extract info from the first layer to define a list of inputs
    first_layer = layers[0]
    weights, _ = get_info(first_layer)
    num_inputs = len(weights)
    input_list = [library.Real('X_' + str(i)) for i in range(num_inputs)]

    # Iterate through layers to determine the neurons in each layer
    for index in range(len(layers) - 1):
        # Get the layer info
        layer = layers[index]
        weights, bias = get_info(layer)
        num_neurons = len(weights[0])

        # Define the neuron list
        neuron_list = [library.Real('n' + str(index) + '_' + str(x)) for x in range(num_neurons)]
        for i in range(len(neuron_list)):
            # Find the sum weights of a neuron
            total = weights[0][i] * input_list[0]
            for input in range(1, len(input_list)):
                total += (weights[input][i] * input_list[input])

            # Add bias and clean up the formula
            total += bias[i][0]
            total = library.simplify(total)

            # Append the constraint into the list
            constraint_list.append(neuron_list[i] == library.If(total <= 0, 0, total))

        # The current neuron list becomes the inputs for the next layer
        input_list = neuron_list

    # Extract info from the last layer to define a list of outputs
    last_layer = layers[-1]
    weights, bias = get_info(last_layer)
    num_outputs = len(weights[0])
    output_list = [library.Real('Y_' + str(i)) for i in range(num_outputs)]

    for i in range(len(output_list)):
        # Find the sum weights of the final outputs
        total = weights[0][i] * input_list[0]
        for input in range(1, len(input_list)):
            total += (weights[input][i] * input_list[input])
        total += bias[i][0]
        total = library.simplify(total)

        # Append the outputs into the list
        constraint_list.append(output_list[i] == total)

    return library.And(constraint_list)

def create_random(layers, interval = [-5, 5]) -> Sequential:
    """
    Create a DNN with random weights and biases from provided layers and intervals for random float number
    Args:
        layers: a list of number of neurons
        interval: a number interval
    """
    inputs = layers[0]
    model = Sequential()
    prev_nodes = inputs
    for i in range(1, len(layers)):
        nodes = layers[i]

        # set up weights and bias
        weights = []
        bias = []
        for _ in range(prev_nodes):
            curr = []
            for _ in range(nodes):
                curr.append(random.uniform(interval[0], interval[1]))
            weights.append(curr)
        for _ in range(nodes):
            bias.append([random.uniform(interval[0], interval[1])])

        # set up inputs for first hidden layer
        if i == 1:
            dense = Dense(units = nodes,
                      input_shape = (inputs, ),
                      kernel_initializer = tf.constant_initializer(weights),
                      bias_initializer = tf.constant_initializer(bias),
                      dtype='float64')
        # the output layer has no activation function
        elif i == len(layers) - 1:
            dense = Dense(units = nodes,
                activation = None,
                kernel_initializer = tf.constant_initializer(weights),
                bias_initializer = tf.constant_initializer(bias),
                dtype='float64')
        # the rest
        else:
            dense = Dense(units = nodes,
                activation = activations.relu,
                kernel_initializer = tf.constant_initializer(weights),
                bias_initializer = tf.constant_initializer(bias),
                dtype='float64')

        # update the previous number of nodes
        prev_nodes = nodes
        model.add(dense)

    return model
