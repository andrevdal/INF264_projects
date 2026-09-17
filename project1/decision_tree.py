# 1 Decision Trees ---
import numpy as np

#1.1 The ID3 Algorithm 

class DecisionTree:
    def __init__(self, criterion="entropy", maxDepth=None):
        self.criterion = criterion
        self.maxDepth = maxDepth
        self.root = None  # holds the tree structure once fit() executes

    def fit(self, X, y):
        ...

    def predict(self, X):
        ...


def entropy(y):
    _, classCount = np.unique(y, return_counts = True) #returns the number of times each class occured as a array
    accumulatedSum = 0
    
    for count in classCount: 
        p = count /len(y)   #proportion of each class
        entropyTerm = -p * np.log2(p)  #calculating entropy for each class
        accumulatedSum += entropyTerm 
        
    return accumulatedSum

def bestSplit(X, y, impurityFunction):
    ...


def buildTree(X, y, depth, maxDepth, impurityFunction):
    #1.3 Maximum Depth: 
    # hvis depth == max_depth -> løvnode med mest vanlige label
    ...


def predictOne(x, node):
    ...


#1.2 The Gini Index

def gini(y):
    _, classCount = np.unique(y, return_counts = True) #returns the number of times each class occured as a array
    accumulatedSum = 1
    
    for count in classCount: 
        p = count /len(y)   #proportion of each class
        giniTerm = p ** 2   #calculating gini for each class
        accumulatedSum -= giniTerm 
        
    return accumulatedSum