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

TableOfData = pd.read_csv("C:/Users/smith/OneDrive/Documents/GitHub/Machine-learning-experiments/Exoplanets/EP&FP_RemovedColumns.csv", error_bad_lines=False)

numberOfSucesses = 0
learningRate = 0.02
parameters = []

for i in range(1, TableOfData.shape[1]):
    parameters.append(0.0)

def HypothesisFunction(parameters):
    """Finds the hypothesis function, which is a function between 0 and 1"""
    lineOfBestFit = []
    hypotheses = []
    for row in range(TableOfData.shape[0]):
        sumOfxTheta = 0.0
        for column in range(len(parameters)):
            sumOfxTheta += parameters[column]*TableOfData.iloc[row, column + 1]
        lineOfBestFit.append(sumOfxTheta)
        hypotheses.append(1/(1 + np.exp(-lineOfBestFit[row])))
    return hypotheses


def CostFunction(parameters):
    """Calculates the cost function including the the differences between y=1 and y=0"""
    hypotheses = HypothesisFunction(parameters)
    cCost = []
    jCost = 0.0
    for row in range(TableOfData.shape[0]):
        if TableOfData.iloc[row,0] == 1:
            cCost.append(-np.log(hypotheses[row]))
        elif TableOfData.iloc[row,0] == 0:
            cCost.append(-np.log(1 - hypotheses[row]))

    for item in cCost:
        jCost += (1/len(cCost))*(item)

    return jCost


def SingleParameterAdjust(parameters, columnValue, learningRate):
    """Uses the derivative of the cost function to change a single parameter"""
    exponetialWithPositiveSum = []
    for row in range(TableOfData.shape[0]):
        sumOfxTheta = 0.0
        for column in range(len(parameters)):
            sumOfxTheta += parameters[column]*TableOfData.iloc[row, column+1]
        exponetialWithPositiveSum.append(sumOfxTheta)

    trialParameter = 0.0
    adjustmentAmount = 0.0
    for row in range(TableOfData.shape[0]):
        if TableOfData.iloc[row,0] == 1:
            adjustmentAmount += (1/TableOfData.shape[0])*TableOfData.iloc[row, columnValue+1]/(exponetialWithPositiveSum[row] + 1)
        elif TableOfData.iloc[row,0] == 0:
            adjustmentAmount -= (1/TableOfData.shape[0])*TableOfData.iloc[row, columnValue+1]*exponetialWithPositiveSum[row]/(exponetialWithPositiveSum[row] + 1)
    
    trialParameter = parameters[columnValue] + learningRate*adjustmentAmount
    return trialParameter


def TotalParameterAdjust(parameters, numberOfSucesses, hypotheses, learningRate):
    """Runs the single parameter adjust function on all the parameters"""
    newParameters = [0.0]*len(parameters)
    for column in range(len(parameters)):
        newParameters[column] = SingleParameterAdjust(parameters, column, learningRate)
    return newParameters


def ParameterEvaluator(parameters, cost, numberOfSucesses, hypotheses, learningRate):
    """This function will return the optimum parameters"""
    newParameters = TotalParameterAdjust(parameters, numberOfSucesses, hypotheses, learningRate)
    newCost = CostFunction(newParameters)
    if newCost <= cost:
        print("First Attempt Successful")
        return newParameters, newCost
    else:
        print("First Attempt Unsuccessful")
        print("Produced Cost: ", newCost)
        newNewParameters = TotalParameterAdjust(newParameters, numberOfSucesses, hypotheses, learningRate)
        newNewCost = CostFunction(newNewParameters)
        if newNewCost > cost:
            print("Second Attempt Unsuccessful")
            print("Produced Cost: ", newNewCost)
            return parameters, cost
        else:
            print("Second Attempt Succesful")
            return newNewParameters, newNewCost


def AccuracyEvaluator(parameters, numberOfSucesses):
    hypotheses = HypothesisFunction(parameters)
    for row in range(TableOfData.shape[0]):
        if (hypotheses[row] >= 0.75 and TableOfData.iloc[row,0] == 1):
            numberOfSucesses += 1
        elif (hypotheses[row] <= 0.25 and TableOfData.iloc[row,0] == 0):
            numberOfSucesses += 1
    return numberOfSucesses, hypotheses


hypotheses = HypothesisFunction(parameters)
cost = CostFunction(parameters)
numberOfSucesses, hypotheses = AccuracyEvaluator(parameters, numberOfSucesses)
trials = 1
print(cost)
print(numberOfSucesses)

while (numberOfSucesses < 5000 and trials <= 1000):
    parameters, newCost = ParameterEvaluator(parameters, cost, numberOfSucesses, hypotheses, learningRate)
    numberOfSucesses, hypotheses = AccuracyEvaluator(parameters, numberOfSucesses)
    if newCost == cost:
        print("Maximum improvement reached")
        break
    else:
        cost = newCost
        trials += 1
        print("Trial Complete")
        print(cost)

print(cost)
print(parameters)
print(numberOfSucesses)