import copy
import sys
import numpy
import math

# e.g. score on a pass/fail test, 70% pass
xs = [89, 46, 67, 75, 93, 21, 5, 54, 81, 36, 77, 14]
ys = [1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0]
params = [2, 2]

def LogisticHyp(params, trainx, index):
    
    z = params[0]
    for i in range(1, len(params)):
        z += params[i] * trainx[index]#[i-1]

    ans = 1 / (1 + math.exp(-z))
    return ans, z


def CostCalc(h, trainy, index):
    ans = 0
    yisOne = False
    if trainy[index] == 1:
        ans = -numpy.log(h)
        #print(ans)
        yisOne = True
    elif trainy[index] == 0:
        ans = -numpy.log(1 - h)
        #print(ans)
    else:
        raise ValueError('Training outputs must be equal to either 0 or 1.')
    
    return ans, yisOne


def CostFunction(params, trainx, trainy):
    cost = 0

    for i in range(len(trainx)):
        hyp, foo = LogisticHyp(params, xs, i)
        print(f'hyp = {hyp}')
        adder, bar = CostCalc(hyp, ys, i)
        cost += adder
    cost = cost / len(trainx)

    return cost


def GradAdjust(params, pIndex, trainx, trainy, rate):
    grad = 0
    ans = params[pIndex]

    for i in range(len(trainx)):
        hyp, z = LogisticHyp(params, trainx, i)
        grad += math.exp(-z) * 1 / ((1 + math.exp(-z))**2)

        if trainy[i] == 1:
            grad = -grad * 1 / hyp
        elif trainy[i] == 0:
            grad = grad * 1 / (1 - hyp)
        else:
            raise ValueError('Training output data must take value of 0 or 1.')
        if pIndex != 0:
            grad = grad * trainx[i]

    ans -= rate * grad
    return ans




def gradDescent(params, trainx, trainy, rate):
    """Recursive function that converges on optimum parameters for cost minimisation."""
    
    refCost = CostFunction(params, trainx, trainy)
    temp = copy.deepcopy(params)

    # apply descent
    for i in range(len(params)):
        temp[i] = GradAdjust(temp, i, xs, ys, rate)
    
    newCost = CostFunction(temp, trainx, trainy)
    # compare to previous cost
    if newCost / refCost < 1.00000001 and newCost / refCost > 0.999999999:
        print('Within acceptable bounds')
        return params
    elif newCost < refCost:
        params = temp
        print(params)
        gradDescent(params, trainx, trainy, rate)
    elif newCost > refCost:
        print('Initial learning rate too large')
        return refCost

gradDescent(params, xs, ys, float(sys.argv[1]))