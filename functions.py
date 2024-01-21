# imports
import parameters
import classes

import math
import random

# math functions
def create_matrix(n_rows, n_cols, init_function):
    return [[init_function() for _ in range(n_cols)] for _ in range(n_rows)]

def flattenMatrix(matrix):

    if not isinstance(matrix, list):
        return [matrix]
    
    flattened_vector = []
    for element in matrix:
        flattened_vector.extend(flattenMatrix(element))

    return flattened_vector

def mean(array):
    return sum(array) / len(array)

def sample_variance(sample):
    if len(sample) < 2:
        print("ERROR: Variance is not defined for a sample with fewer than 2 elements")
        return 0
    
    return sum((x - mean(sample)) ** 2 for x in sample) / (len(sample) - 1)

# activation functions
def activationFunction_linear(x):
    return x

def activationFunction_threshold(x):
    return x < 0.5

def activationFunction_sigmoid(x):
    return 1 / (1 + math.exp(-x))

# neural network micro functions
def c_axonPotential(c_pre, a_preToPost):
    return c_pre * a_preToPost

def c_postActivation(C_axonPotential):
    return parameters.activationFunction(sum(C_axonPotential))

def a_initWeight():
    return random.random() # random number 0 to 1

# neural metwork validation functions
def validate_hebbian(letters_outputArrays):
    
    # print mean/sample variance of each letter charge
    for i_letter in letters_outputArrays:
        
        letter = classes.letters[i_letter]

        outputArray = letters_outputArrays[i_letter]
        
        print(f"Letter {letter}")
        print(f"--Mean: {mean(outputArray)}")
        print(f"--Variance: {sample_variance(outputArray)}")
    
    # print sample variance of n random samples
    nSamples = 10
    flattenedMatrix = flattenMatrix(letters_outputArrays)
    randomMeans = []
    randomVariances = []
    for _ in nSamples:
        randomSample = random.sample(flattenedMatrix, parameters.nhalf_D)
        randomMeans.extend(mean(randomSample))
        randomVariances.extend(sample_variance(randomSample))

    print(f"{nSamples} random sample average")
    print(f"--Mean: {mean(randomMeans)}")
    print(f"--Variance: {mean(randomVariances)}")

def validate_delta():
    print("Not yet implemented")

# neural network propagation functions

def C_fwdProp(C_pre, npre_npost_a):
    
    # set up pre/postsynaptic neuron counts
    n_pre = len(C_pre)
    n_post = len(npre_npost_a[0])

    # calculate axon potentials
    npre_npost_caxonPotential = [] # there are n_pre arrays of n_post axon potentials                    
    for i_pre in range(n_pre):
        c_pre = C_pre[i_pre]
        npre_npost_caxonPotential.extend([])
        npost_caxonPotential = npre_npost_caxonPotential[i_pre] # there are n_post axon potentials
        for i_post in range(n_post):
            a_preToPost = npre_npost_a[i_pre][i_post]
            c_axonPotential = c_axonPotential(c_pre, a_preToPost)
            npost_caxonPotential.extend(c_axonPotential)
    
    # calculate postsynaptic action potential
    C_postActivation = []
    for i_post in range(n_post):
        C_postAxonPotentials = npre_npost_caxonPotential[:][i_post]
        C_postActivation.extend(c_postActivation(C_postAxonPotentials))
    
    # return c_postActivation
    return C_postActivation
