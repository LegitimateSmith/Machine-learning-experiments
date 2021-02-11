import copy
import sys
import numpy as np
import math
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame
import seaborn as sns
import random

pd.set_option('display.max_columns', None)

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

dataFrame = pd.read_csv("C:/Users/smith/OneDrive/Documents/GitHub/Machine-learning-experiments/Exoplanets/Exoplanets_and_false_positives.csv", error_bad_lines=False)

successRate = 0.0
successPercentage = 0.0
parameter = []
sumFunction = [0]*dataFrame.shape[0]

for i in range(1, dataFrame.shape[1]):
    parameter.append(random.randint(-2,1)+random.random())

def additionFunction(sumFunction, parameter):
    for j in range(dataFrame.shape[0]):
        for i in range(1, dataFrame.shape[1]):
            sumFunction[j] = sumFunction[j] + parameter[i-1]*dataFrame.iloc[j,i]
    return sumFunction

def evalutorFunction(sumFunction, successRate):
    for i in range(len(sumFunction)):
        if (sumFunction[i] >= 1 and dataFrame.iloc[i,0] == 1):
            successRate = successRate + 1
        elif (sumFunction[i] < 1 and dataFrame.iloc[i,0] == 0):
            successRate = successRate + 1
    return successRate

def parameterAdjust(parameter, sumFunction, successRate, counterForTrials):
    parameterTrial1 = []
    parameterTrial2 = []
    parameterTrial3 = []
    
    for i in range(len(parameter)):
        improvement = False
        timesImproved = 1
        while improvement == False and timesImproved <=10:
            sumFunctionTrial1 = [0.0]*dataFrame.shape[0]
            sumFunctionTrial2 = [0.0]*dataFrame.shape[0]
            sumFunctionTrial3 = [0.0]*dataFrame.shape[0]
            successRateTrial1 = 0
            successRateTrial2 = 0
            successRateTrial3 = 0

            parameterTrial1.append(parameter[i] + (2*timesImproved + random.random())/(counterForTrials + 1))
            parameterTrial2.append(parameter[i] - (2*timesImproved - random.random())/(counterForTrials + 1))
            parameterTrial3.append((parameter[i]/(2*timesImproved*(counterForTrials+1))))

            for j in range(dataFrame.shape[0]):
                sumFunctionTrial1[j] = sumFunction[j] + (parameterTrial1[i] - parameter[i])*dataFrame.iloc[j,i]
                sumFunctionTrial2[j] = sumFunction[j] + (parameterTrial2[i] - parameter[i])*dataFrame.iloc[j,i]
                sumFunctionTrial3[j] = sumFunction[j] + (parameterTrial3[i] - parameter[i])*dataFrame.iloc[j,i]

            successRateTrial1 = evalutorFunction(sumFunctionTrial1, successRateTrial1)

            if successRateTrial1 >= successRate:
                parameter[i] = parameterTrial1[i]
                successRate = successRateTrial1
                improvement = True
                print("Successful Improvement")
                continue

            successRateTrial2 = evalutorFunction(sumFunctionTrial2, successRateTrial2)
            
            if successRateTrial2 >= successRate:
                parameter[i] = parameterTrial2[i]
                successRate = successRateTrial2
                improvement = True
                print("Successful Improvement")
                continue

            successRateTrial3 = evalutorFunction(sumFunctionTrial3, successRateTrial3)

            if successRateTrial3 >= successRate:
                parameter[i] = parameterTrial3[i]
                successRate = successRateTrial3
                improvement = True
                print("Successful Improvement")
                continue

            timesImproved += 1
        print(i)

    return parameter, successRate



sumFunction = additionFunction(sumFunction, parameter)
successRate = evalutorFunction(sumFunction, successRate)
successPercentage = (successRate/dataFrame.shape[0])*100
counterForTrials = 0

while counterForTrials < 1:  
    parameter, successRate = parameterAdjust(parameter, sumFunction, successRate, counterForTrials)

    successPercentage = (successRate/dataFrame.shape[0])*100
    counterForTrials = counterForTrials + 1
    print("Trials Completed:", counterForTrials)
    print("Current Accuracy:", successPercentage, "%")


fileParametersArray = np.load("C:/Users/smith/OneDrive/Documents/GitHub/Machine-learning-experiments/Exoplanets/Parameters.npy", allow_pickle = True)
fileParameters = fileParametersArray.tolist()

if fileParameters[-1] <= successRate:
    print("The Stored Success Rate Is Lower Than The Current One")
    print("These Parameters Will Be Saved")
    parametersAndSR = parameter
    parametersAndSR.append(float(successRate))
    np.save("C:/Users/smith/OneDrive/Documents/GitHub/Machine-learning-experiments/Exoplanets/Parameters.npy", parametersAndSR, allow_pickle = True)
    if parameter[-1] > 1000:
        del parameter[-1]
else:
    print("The Stored Success Rate Is Higher Than The Current One")
    print("The Stored Parameter Will Remain The Same")
    successRate = fileParameters[-1]
    del fileParameters[-1]
    parameter = fileParameters

print(len(parameter))
print("The Optimum Parameters Are:")
print(parameter)
successPercentage = (successRate/dataFrame.shape[0])*100
print("The best success percentage:", successPercentage, "%")