from keras.models import Sequential
from keras.layers import Dense
from keras import activations
import tensorflow as tf

def read_spec(library, filename= "acasxu/spec/prop_1.vnnlib"):
    file = open(filename)
    variable_dict = dict()
    pre_list = []
    post_list = []

    for line in file:
        line = line.strip()

        # Skip empty or comment lines
        if line == "" or line.startswith(";"):
            continue

        line = line[1:-1]
        if line.startswith("declare-const"):
            parse_line = line.split()
            variable_name = parse_line[1]
            type = parse_line[2]
            if type == "Real":
                variable_dict[variable_name] = library.Real(variable_name)
        elif line.startswith("assert"):
            op, variable_name, value = line[8:-1].split()
            if value.startswith("X") or value.startswith("Y"):
                value = variable_dict[value]
            else:
                value = eval(value)
            if op == ">=":
                if variable_name.startswith("X"):
                    change_list = pre_list
                elif variable_name.startswith("Y"):
                    change_list = post_list
                change_list.append(variable_dict[variable_name] >= value)
            elif op == "<=":
                if variable_name.startswith("X"):
                    change_list = pre_list
                elif variable_name.startswith("Y"):
                    change_list = post_list
                change_list.append(variable_dict[variable_name] <= value)

    file.close()
    return (library.And(pre_list), library.And(post_list))

def readNNet(filename: str) -> Sequential:
    """
    Return a DNN based on the information from the provided file
    Args:
        file (type: str): filename that provides information about NNet
    """
    file = open(filename)

    # Skip header lines
    line = file.readline()
    while line.startswith("//"):
        line = file.readline()

    parse_line = line.split(",")
    num_layers = int(parse_line[0])
    num_inputs = int(parse_line[1])

    line = file.readline()
    parse_line = line.split(",")

    layers = []
    for i in range(num_layers + 1):
        layers.append(int(parse_line[i]))

    # Skip line containing "0,"
    file.readline()

    # Read the normalization information
    line = file.readline()
    inputMins = [float(x) for x in line.strip().split(",")[:-1]]

    line = file.readline()
    inputMaxes = [float(x) for x in line.strip().split(",")[:-1]]

    line = file.readline()
    means = [float(x) for x in line.strip().split(",")[:-1]]

    line = file.readline()
    ranges = [float(x) for x in line.strip().split(",")[:-1]]

    model = Sequential()
    for i in range(1, num_layers + 1):
        nodes = layers[i]
        prev_nodes = layers[i - 1]

        weights = [[] for x in range(prev_nodes)]
        biases = []

        for _ in range(nodes):
            line = file.readline()
            weight_list = [float(x) for x in line.strip().split(",")[:-1]]
            for w in range(prev_nodes):
                weights[w].append(weight_list[w])

        for _ in range(nodes):
            line = file.readline()
            biases.append([float(line.strip().split(",")[0])])
        if i == 1:
            dense = Dense(units = nodes,
                        input_shape = (num_inputs, ),
                        kernel_initializer = tf.constant_initializer(weights),
                        bias_initializer = tf.constant_initializer(biases),
                        dtype='float64')
        # the output layer has no activation function
        elif i == num_layers:
            dense = Dense(units = nodes,
                activation = None,
                kernel_initializer = tf.constant_initializer(weights),
                bias_initializer = tf.constant_initializer(biases),
                dtype='float64')
        # the rest
        else:
            dense = Dense(units = nodes,
                activation = activations.relu,
                kernel_initializer = tf.constant_initializer(weights),
                bias_initializer = tf.constant_initializer(biases),
                dtype='float64')

        model.add(dense)
    file.close()
    return model
