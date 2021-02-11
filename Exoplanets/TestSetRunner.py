import copy
import sys
import numpy as np
import math
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import random

fileParametersArray = np.load("C:/Users/smith/OneDrive/Documents/GitHub/Machine-learning-experiments/Exoplanets/Parameters.npy", allow_pickle = True)
parameter = fileParametersArray.tolist()

del parameter[-1]

pd.set_option('display.max_columns', None)

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

dataFrame = pd.read_csv("C:/Users/smith/OneDrive/Documents/GitHub/Machine-learning-experiments/Exoplanets/ExoplanetsTrialDataset.csv", error_bad_lines=False)

sumFunction = [0.0]*dataFrame.shape[0]

for j in range(dataFrame.shape[0]):
        for i in range(1, dataFrame.shape[1]):
            sumFunction[j] = sumFunction[j] + parameter[i-1]*dataFrame.iloc[j,i]

successRate = 0

for i in range(len(sumFunction)):
        if (sumFunction[i] >= 1 and dataFrame.iloc[i,0] == 1):
            successRate = successRate + 1
        elif (sumFunction[i] < 1 and dataFrame.iloc[i,0] == 0):
            successRate = successRate + 1


print((successRate/dataFrame.shape[0])*100)