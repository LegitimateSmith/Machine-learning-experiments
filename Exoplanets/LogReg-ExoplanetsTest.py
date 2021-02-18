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
    #This sets the starting values for the parameters
    #parameter.append(random.randint(-2,1)+random.random())
    parameter.append(0.0)

def additionFunction(sumFunction, parameter):
    """This function, for each row, finds the sum of the products of the parametrs and their associated row"""
    for row in range(dataFrame.shape[0]):
        for column in range(1, dataFrame.shape[1]):
            sumFunction[row] = sumFunction[row] + parameter[column-1]*dataFrame.iloc[row,column]
    return sumFunction

def evalutorFunction(sumFunction, successRate):
    """evalutaor function defines the values for which the sum function corresponds to an exoplant or not and checks that against the values in the table"""
    print("Called")
    for i in range(len(sumFunction)):
        if (sumFunction[i] >= 1 and dataFrame.iloc[i,0] == 1):
            successRate = successRate + 1
        elif (sumFunction[i] < 1 and dataFrame.iloc[i,0] == 0):
            successRate = successRate + 1
        if i < 10:
            print(f'Sum = {sumFunction[i]}\n Actual value = {dataFrame.iloc[i,0]} \n Success no. = {successRate}')
    return successRate

def parameterAdjust(parameter, sumFunction, successRate, counterForTrials):
    """This function creates new parameters to try against the existing ones"""
    parameterTrial1 = []
    parameterTrial2 = []
    parameterTrial3 = []
    parameterTrial4 = []
    
    for i in range(len(parameter)):
        improvement = False
        timesImproved = 1
        while improvement == False and timesImproved <=1:
            #All the new parameters need sum functions and success rates
            sumFunctionTrial1 = [0.0]*dataFrame.shape[0]
            sumFunctionTrial2 = [0.0]*dataFrame.shape[0]
            sumFunctionTrial3 = [0.0]*dataFrame.shape[0]
            sumFunctionTrial4 = [0.0]*dataFrame.shape[0]
            successRateTrial1 = 0
            successRateTrial2 = 0
            successRateTrial3 = 0
            successRateTrial4 = 0

            parameterTrial1.append(parameter[i] + (timesImproved + random.random())/(counterForTrials + 1))
            parameterTrial2.append(parameter[i] - (timesImproved + random.random())/(counterForTrials + 1))
            parameterTrial3.append((parameter[i]/(2*timesImproved*(counterForTrials+1))))
            parameterTrial4.append(random.randint(-3,2)+random.random())

            for j in range(dataFrame.shape[0]):
                #This is the equivalent of addition function however slightly faster as the base values are known so its the difference that is calculated
                sumFunctionTrial1[j] = sumFunction[j] + (parameterTrial1[i] - parameter[i])*dataFrame.iloc[j,i]
                sumFunctionTrial2[j] = sumFunction[j] + (parameterTrial2[i] - parameter[i])*dataFrame.iloc[j,i]
                sumFunctionTrial3[j] = sumFunction[j] + (parameterTrial3[i] - parameter[i])*dataFrame.iloc[j,i]
                sumFunctionTrial4[j] = sumFunction[j] + (parameterTrial4[i] - parameter[i])*dataFrame.iloc[j,i]

            #The statements below determine if any of the new sum functions have a higher success rate

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

            successRateTrial4 = evalutorFunction(sumFunctionTrial4, successRateTrial4)

            if successRateTrial4 >= successRate:
                parameter[i] = parameterTrial4[i]
                successRate = successRateTrial4
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

while counterForTrials < 3:  
    parameter, successRate = parameterAdjust(parameter, sumFunction, successRate, counterForTrials)

    successPercentage = (successRate/dataFrame.shape[0])*100
    counterForTrials = counterForTrials + 1
    print("Trials Completed:", counterForTrials)
    print("Current Accuracy:", successPercentage, "%")

 
#parametersAndSR = parameter
#parametersAndSR.append(float(successRate))
#np.save("C:/Users/smith/OneDrive/Documents/GitHub/Machine-learning-experiments/Exoplanets/ParametersFromTrials/160221-ZeroStarting-LR15.npy", parametersAndSR, allow_pickle = True)
#if parameter[-1] > 1000:
    #del parameter[-1]


print(len(parameter))
print("The Optimum Parameters Are:")
print(parameter)
successPercentage = (successRate/dataFrame.shape[0])*100
print("The best success percentage:", successPercentage, "%")