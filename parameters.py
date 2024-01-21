# imports
import functions
import dataset
import classes

import random

# ---STATIC

# hiddenLayers
n_hiddenLayers = 5
n_hidden = 10

# outputs
n_outputs = 1 # do not change yet

# functions
learningAlgorithm = classes.learningAlgorithm.Hebbian
activationFunction = functions.activationFunction_sigmoid

# learning parameters
n_epochs = 5
learningRate = 0.01

# ---PROCEDURAL

# set up input data
n_inputs = len(functions.flattenMatrix(dataset.D[0][0]))

# set up training/testing data
nhalf_D = len(dataset.D[0]) // 2
TR = []
TE = []
for d in dataset.D:
    random.shuffle(d)
    TR.extend([d[:nhalf_D]])
    TE.extend([d[nhalf_D:]])
