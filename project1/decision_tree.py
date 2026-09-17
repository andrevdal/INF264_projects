# 1 Decision Trees ---

import numpy as np

#1.1 The ID3 Algorithm 

class DecisionTree:
    def __init__(self, criterion="entropy", max_depth=None):
        self.criterion = criterion
        self.max_depth = max_depth
        self.root = None  # holds the tree structure once fit() executes

    def fit(self, X, y):
        ...

    def predict(self, X):
        ...


def entropy(y):
    ...


def best_split(X, y, impurity_function):
    ...


def build_tree(X, y, depth, max_depth, impurity_function):
    # stoppbetingelser her, blant annet:
    # 1.3 Maximum Depth: hvis depth == max_depth -> løvnode med mest vanlige label
    ...


def predict_one(x, node):
    ...


#1.2 The Gini Index

def gini(y):
    ...