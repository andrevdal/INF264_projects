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
    # for each unique class c in y:
    #     p = andel av y som er c
    #     akkumuler -p * log2(p)   (hopp over p=0)
    # return akkumulert sum
    
    uniqueClasses, numberOfEach = 


def best_split(X, y, impurityFunction):
    ...


def buildTree(X, y, depth, maxDepth, impurityFunction):
    #1.3 Maximum Depth: 
    # hvis depth == max_depth -> løvnode med mest vanlige label
    ...


def predictOne(x, node):
    ...


#1.2 The Gini Index
def gini(y):
    # sum = 1
    # for each unique class c in y:
    #     p = andel av y som er c
    #     sum = sum - p^2
    # return sum