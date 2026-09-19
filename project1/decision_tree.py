# 1 Decision Trees ---

import numpy as np

#1.1 The ID3 Algorithm 
class Node:
    def __init__(
            self,
            featureIndex = None,
            threshold = None,
            left = None,
            right = None,
            value = None,
    ):
        self.featureIndex = featureIndex
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value

    def isLeaf(self): #seperates nodes, True for a leaf node, False for an inner node
        return self.value is not None 


class DecisionTree:
    def __init__(
            self, 
            criterion="entropy", 
            max_depth=None
    ):
        self.criterion = criterion
        self.max_depth = max_depth
        self.root = None  # holds the tree structure once fit() executes

    def fit(self, X, y):
        self.root = buildTree(X, y, 0, self.max_depth, impurityFunction = entropy if self.criterion == "entropy" else gini)

    def predict(self, X):
        #predicting one row at a time
        return [predictOne(row, self.root) for row in X]


def entropy(y):
    _, classCount = np.unique(y, return_counts = True) #returns the number of times each class occured as a array
    accumulatedSum = 0
    
    for count in classCount: 
        p = count /len(y)   #proportion of each class
        entropyTerm = -p * np.log2(p)  #calculating entropy for each class
        accumulatedSum += entropyTerm 
        
    return accumulatedSum


def bestSplit(X, y, impurityFunction): #X = features, y = labels, impurityFunction = entropy/gini

    impurityBeforeSplit = impurityFunction(y) 
    best = (float('-inf'), None, None)   #(-infinity, index, threshold)

    for i in range(X.shape[1]):
        columnValues = X[:, i]  #gets each column from the features
        threshold = np.mean(columnValues) 

        mask = columnValues <= threshold #testing the spesific feature against the theshold to make a True/False array mask
        y_left = y[mask] 
        y_right = y[~mask] #~ inverts the mask

        #if one of the groups = 0, the split didn't work, so skip this candidate
        if len(y_left) == 0 or len(y_right) == 0:
            continue
        
        impurityLeft = impurityFunction(y_left)
        impurityRight = impurityFunction(y_right)

        weightedImpurity = (len(y_left)/len(mask) * impurityLeft + (len(y_right)/len(mask) * impurityRight))

        #update best candidates, only if we get a bigger gain
        gain = impurityBeforeSplit - weightedImpurity
        if best[0] < gain:
            best = (gain, i, threshold)

    return best #return the gain, the index of the feature and the threshold


def buildTree(X, y, depth, max_depth, impurityFunction):

    #finds most common label
    uniqueClasses, classCount = np.unique(y, return_counts=True)
    mostCommon = uniqueClasses[np.argmax(classCount)] 

    #Criteria for leaf-nodes
    if len(np.unique(y)) == 1: #is all the labels in y the same?
        return Node(value = y[0]) #leaf node

    elif len(np.unique(X, axis=0)) == 1: #is all the rows identical in X?
        return Node(value = mostCommon) #leaf node

    elif max_depth == depth: #1.3 Maximum Depth
        return Node(value = mostCommon) #leaf node

    #split the data
    _, featureIndex, threshold  = bestSplit(X, y, impurityFunction)

    #if no split worked, we wont have any values
    if featureIndex is None: 
        return Node(value = mostCommon) #leaf node

    mask = X[:, featureIndex] <= threshold #testing the feature from X against the threshold to make a True/False array mask

    X_left = X[mask]
    y_left = y[mask]

    X_right = X[~mask]
    y_right = y[~mask]

    #recrusive call to build tree on both halves
    leftSubTree = buildTree(X_left, y_left, depth +1, max_depth, impurityFunction)
    rightSubTree = buildTree(X_right, y_right, depth +1, max_depth, impurityFunction)

    #make inner node
    innerNode = Node(featureIndex=featureIndex, threshold=threshold, left=leftSubTree, right=rightSubTree)
    return innerNode


def predictOne(x, node): 
    if node.isLeaf():
        return node.value

    elif x[node.featureIndex] <= node.threshold:
        return predictOne(x, node.left)
    else:
        return predictOne(x, node.right)


#1.2 The Gini Index
def gini(y):
    _, classCount = np.unique(y, return_counts = True) #returns the number of times each class occured as a array
    accumulatedSum = 1
    
    for count in classCount: 
        p = count /len(y)   #proportion of each class
        giniTerm = p ** 2   #calculating gini for each class
        accumulatedSum -= giniTerm 
        
    return accumulatedSum




# 3 Feature Importance ---

def permutation_importance(model, X, y, metric, n_repeats, seed):
    baseline = metric(y, model.predict(X))
    rng = np.random.default_rng(seed)

    importanceScores = np.zeros((X.shape[1], n_repeats)) #starts as zeroes

    for j in range(X.shape[1]):
        X_permuted = X.copy() #new copy for every feature

        for n in range(n_repeats):
            X_permuted[:, j] = rng.permutation(X[:, j]) #ransomly permute the selected column
            featureScore = metric(y, model.predict(X_permuted)) #make new score with the permuted column

            importanceScores[j, n] = baseline - featureScore # high positive score = used that feature a lot, so it's important
                                                             # low positive score = feature was not important
                                                             # negative score = coincidentally made model slighty better. This is usually just noise and means the feature is not important
    return importanceScores                 

