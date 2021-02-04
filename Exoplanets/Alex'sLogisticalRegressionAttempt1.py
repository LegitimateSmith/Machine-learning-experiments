import copy
import sys
import numpy as np
import math
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

testScores = [89, 46, 67, 75, 93, 21, 5, 54, 81, 36, 77, 14]
passOrFail = [1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0]
parameter = 1.0
trialPassOrFail = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
successRate = 0

sumOfScores = 0.0

for i in range(len(testScores)):
    sumOfScores += testScores[i]

for i in range(len(testScores)):
    testScores[i] = testScores[i]/(sumOfScores/len(testScores))

print(testScores)

def additionFunction(testScores, trialPassOrFail, parameter):
    
    for i in range(len(testScores)):
        cost = (testScores[i]) * parameter
        if cost >= 5:
            trialPassOrFail[i] = 1
        else:
            trialPassOrFail[i] = 0
    return trialPassOrFail

def effectivenessEvaluator(passOrFail, trialPassOrFail, successRate):
    successRate = 0
    for i in range(len(trialPassOrFail)):
        if trialPassOrFail[i] == passOrFail[i]:
            successRate = successRate + 1
    return successRate



def parameterAdjuster(successRate, parameter, testScores, trialPassOrFail, passOrFail):
    tries = 0
    additionFunction(testScores, trialPassOrFail, parameter)
    successRate = effectivenessEvaluator(passOrFail, trialPassOrFail, successRate)
    while (successRate != len(passOrFail) and tries <= 10):
        tries = tries + 1
        previousParameter = parameter
        previousSuccessRate = successRate
        parameter = parameter + len(passOrFail)/successRate
        additionFunction(testScores, trialPassOrFail, parameter)
        successRate = effectivenessEvaluator(passOrFail, trialPassOrFail, successRate)

        if (successRate < previousSuccessRate):
            parameter = previousParameter
            successRate = previousSuccessRate
            break
    print(tries)
    return successRate, parameter

successRate, parameter = parameterAdjuster(successRate, parameter, testScores, trialPassOrFail, passOrFail)
print(successRate, parameter)