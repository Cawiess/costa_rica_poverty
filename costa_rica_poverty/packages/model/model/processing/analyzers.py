import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

from typing import List

from sklearn.feature_selection import VarianceThreshold


'''
Rationale for BaseEstimator and TransformerMixin: as described in preprocessors.py.

How are a analyzers different from preprocessors, and why are they in separate modules?

While preprocessors perform strictly ad-hoc operations on hard coded variables,
analyzers perform actions based on estimates. One example is implementation of 
filter-methods which use measures of variance and association to remove redundant
variables from a dataframe. They deal more with variable selection than data cleaning.

'''

class AnalyzerUnitTemplate(BaseEstimator, TransformerMixin):
    def __init__(self, variables: List[str]) -> None:
        '''
        Specify variable input as list of strings representing column names of a pd.DataFrame.
        '''
        # YOUR CODE HERE
        return None
    
    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        '''
        Required method for Sklearn TransformerMixin class.
        Remains inactive and performs no action for now.
        Leave as is.
        '''
        return self

    def transform(self, X: pd.DataFrame, y: pd.Series = None):
        '''
        Creates a copy of input dataframe, which is passed to method via the sklearn Pipeline.
        This method performs changes to the dataframe with reference to specified variables.
        The modified copy of the original dataframe is then returned and passed to the next step in pipeline.
        Define your specific transformation here.
        '''
        X = X.copy()
        # YOUR CODE HERE

        return X


class VarianceThresholdRemover(BaseEstimator, TransformerMixin):
    ''' Identifies and removes variables with 0 variance. '''
    def __init__(self, variance_threshold: float):
        if not isinstance(variance_threshold, float):
            raise ValueError('Variance threshold must be an integer.')
        
        self.variance_threshold = variance_threshold

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        return self

    def transform(self, X: pd.DataFrame, y: pd.Series = None):
        X = X.copy()

        variance_selector = VarianceThreshold(threshold=self.variance_threshold)
        variance_selector.fit(X)
        constants = X.columns[~variance_selector.get_support()]

        #TODO: Implement logging functionality: which variables are removed and which are kept?

        X = X.drop(constants, axis=1)

        return X