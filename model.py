# imports
import parameters
import functions
import classes
import render

import random

# set up axons

# there are n_inputs arrays of n_hidden axon potentials
ninput_nhidden_a = functions.create_matrix(parameters.n_inputs, parameters.n_hidden, functions.a_initWeight)
# there are n_hiddenLayers of n_hidden arrays of n_hidden axon potentials
nhiddenLayers_nhidden_nhidden_a = [functions.create_matrix(parameters.n_hidden, parameters.n_hidden, functions.a_initWeight) for _ in range(parameters.n_hiddenLayers)]
# there are n_hidden arrays of n_output axon potentials
nhidden_noutput_a = functions.create_matrix(parameters.n_hidden, parameters.n_outputs, functions.a_initWeight)

# train

print(f"BEGINNING {str(parameters.learningAlgorithm)} TRAINING")

for epoch in range(parameters.n_epochs):
    
    print(f"Epoch {epoch}")

    outputs = []

    letter = -1
    for TR_letter in parameters.TR: # each letter's training set
        letter += 1

        print(f"--Letter {letter}")

        outputs.append([])

        random.shuffle(TR_letter)
        
        trial = -1
        for tr_letterMatrix2D in TR_letter: # each individual letter in a random order
            trial += 1

            print(f"----Trial {trial}")

            # INITIALIZE OUTPUT

            c_output = 0
            
            # HEBBIAN LEARNING

            if parameters.learningAlgorithm == classes.learningAlgorithm.Hebbian:

                C_input = functions.flattenMatrix(tr_letterMatrix2D)
                
                C_hiddenLayer1 = functions.C_fwdProp(C_input, ninput_nhidden_a)

                C_nhiddenLayers_hiddenLayerX = []
                C_nhiddenLayers_hiddenLayerX.append(C_hiddenLayer1)
                for i_hiddenLayer in range(1, parameters.n_hiddenLayers):
                    C_nhiddenLayers_hiddenLayerX.append([])
                    C_hiddenLayerPre = C_nhiddenLayers_hiddenLayerX[i_hiddenLayer - 1]
                    C_hiddenLayerPost = functions.C_fwdProp(C_hiddenLayerPre, nhiddenLayers_nhidden_nhidden_a[i_hiddenLayer])
                
                C_output = functions.C_fwdProp(C_nhiddenLayers_hiddenLayerX[-1], nhidden_noutput_a)
                c_output = C_output[0]

            # DELTA LEARNING
                
            elif parameters.learningAlgorithm == classes.learningAlgorithm.Delta:
                print("Delta learning not currently implemented")
            
            # PRINT OUTPUT

            print(c_output)
            outputs[letter].append(c_output)
        
    functions.validate_hebbian(outputs)
    