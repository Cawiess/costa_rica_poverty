import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

from typing import List


'''
Rationale for BaseEstimator and TransformerMixin:

Each project is unique in its details, similar to others in terms of overarching functionality.
Sklearn offers well established functionality which is highly compatible with other services.
Useful core functionalities of Sklearn can be implemented project specific classes through
inheritance of methods from the BaseEstimator and TransformerMixin classes.

By inheriting the methods of the BaseEstimator and TransformerMixin, the preprocessors defined
here can be directly integrated into a Sklearn pipeline.

The user can find a template for a Preprocessing unit which is ready to be extended with
purpose-specific code, as well as a simple usecase below.

'''
######################################### PREPROCESSING UNIT TEMPLATE ###################################
class PreprocessorUnitTemplate(BaseEstimator, TransformerMixin):
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
#######################################################################################################



#################### DATA CLEANING AND CORRECTION ######################
########################################################################

class ColumnLabelNormalizer(BaseEstimator, TransformerMixin):
    def __init__(self):
        '''
        Input: None, iterates over all dataframe columns.
        Normalizes column labels:
            - remove whitespace
            - spaces to _
            - full lowercase
            - remove clutter (ex. ;,.)
        
        
        '''

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        return self

    def transform(self, X: pd.DataFrame):
        
        X = X.copy()
        X.columns = [var.lower() for var in X.columns]
        X.columns = [var.replace(';', '') for var in X.columns]
        X.columns = [var.replace(' ', '_') for var in X.columns]
        
        return X

class ColumnValueNormalizer(BaseEstimator, TransformerMixin):
    def __init__(self):
        '''
        Input: None, iterates over all dataframe columns.
        Normalizes column labels:
            - remove whitespace
            - spaces to _
            - full lowercase
            - remove clutter (ex. ;,.)
            - Check if all remaining column values are numeric, if True; type --> float
        
        
        '''

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        return self

    def transform(self, X: pd.DataFrame):
        
        X = X.copy()
        special_characters = ';:' #TODO: move this to config file

        for variable in X.columns:
            if X[variable].dtype=='O':
                if X[variable].str.contains('|'.join(special_characters)).any():
                    X[variable] = X[variable].str.strip(special_characters)#.astype(bool).any()
                    if X[variable].str.isnumeric().all() == True:
                        X[variable] = X[variable].astype(float)
                        
        return X

class ExtractSubsetVariables(BaseEstimator, TransformerMixin):
    def __init__(self, variables: List[str]):
        ''' Extracts selected variables only. '''

        if not isinstance(variables, list):
            raise ValueError("variables must be given as elements of list.")
        
        self.variables = variables

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        return self

    def transform(self, X: pd.DataFrame):
        
        X = X.copy()
        X = X[self.variables]

        return X

class IntraHouseholdTargetCorrection(BaseEstimator, TransformerMixin):
    def __init__(self, variables: List[str]) -> None:
        if not isinstance(variables, list):
            raise ValueError("variables must be given as elements of list.")
        
        self.variables = variables

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

        # Identify household target mismatches
        householdTargetsMatching = (X.groupby('idhogar')['target'].nunique()==1).reset_index()
        householdTargetMisMatch = householdTargetsMatching[householdTargetsMatching['target']==False]
        
        # set all member targets to head of household target
        for household in householdTargetMisMatch['idhogar']:
            correct_poverty_level = int(X[(X['idhogar'] == household) & (X['parentesco1'] == 1)]['target'])
            X.loc[X['idhogar'] == household, 'target'] = correct_poverty_level

        return X

class HeadOfHouseholdExistCorrection(BaseEstimator, TransformerMixin):
    def __init__(self, variables: List[str]) -> None:
        if not isinstance(variables, list):
            raise ValueError("variables must be given as elements of list.")
        
        self.variables = variables

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
        hh_head = X.groupby('idhogar')['parentesco1'].sum().reset_index()
        hh_head_none= hh_head[hh_head['parentesco1']!=1]
        hh_head_none
        
        X = X[~X['idhogar'].isin(hh_head_none['idhogar'].values)]

        return X

class BinaryEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, variables: List[str]) -> None:
        if not isinstance(variables, list):
            raise ValueError("variables must be given as elements of list.")
        
        self.variables = variables

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
        
        string_to_binary = {"yes": 1, "no": 0}

        X['edjefa'] = X['edjefa'].replace(string_to_binary).astype(float)
        X['edjefe'] = X['edjefe'].replace(string_to_binary).astype(float)
        X['dependency'] = X['dependency'].replace(string_to_binary).astype(float)


        return X

class NumberOfTabletsMissingValues(BaseEstimator, TransformerMixin):
    def __init__(self, variables: List[str]) -> None:
        if not isinstance(variables, list):
            raise ValueError("variables must be given as elements of list.")
        
        self.variables = variables

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

        X['v18q1'] = X['v18q1'].fillna(0)
        print(self.variables)


        return X

class RentMissingValues(BaseEstimator, TransformerMixin):
    def __init__(self, variables: List[str]) -> None:
        if not isinstance(variables, list):
            raise ValueError("variables must be given as elements of list.")
        
        self.variables = variables

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

        # Impute 0 on households that own a house and therefore pay 0 in rent.
        X.loc[(X['tipovivi1'] == 1), 'v2a1'] = 0


        return X

class YearsBehindInSchool(BaseEstimator, TransformerMixin):
    '''
    Variable is only defined for individuals between ages 7-19. 
    Individuals outside this age range are not behind in schooling; their value will be set to 0.

    Documentation specifies that the max value of this variable is 5. 
    Values above 5 will be imputed with 5.
    '''
    def __init__(self, variables: List[str]) -> None:
        if not isinstance(variables, list):
            raise ValueError("variables must be given as elements of list.")
        
        self.variables = variables

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

        # Impute 0 on individuals who are too young or too old for school.
        X.loc[((X['age'] > 19) | (X['age'] < 7)) & (X['rez_esc'].isnull()), 'rez_esc'] = 0

        # Impute 5 where variable exceeds 5.
        X.loc[X['rez_esc'] > 5, 'rez_esc'] = 5


        return X

class DropSquaredVariables(BaseEstimator, TransformerMixin):
    '''
    Dataset is provided whith squared variables and their originals.
    Squared variables may be useful for modelling, but at this stage they are redundant.
    Therefore all squared variables will be dropped.
    '''
    def __init__(self, variables: List[str]) -> None:
        if not isinstance(variables, list):
            raise ValueError("variables must be given as elements of list.")
        
        self.variables = variables

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

        print(self.variables)
        X = X.drop(columns = self.variables)


        return X

class DropHighlyCorrelatedPredictors(BaseEstimator, TransformerMixin):
    '''
    Dataset is provided whith squared variables and their originals.
    Squared variables may be useful for modelling, but at this stage they are redundant.
    Therefore all squared variables will be dropped.
    '''
    def __init__(self, variables: List[str]) -> None:
        if not isinstance(variables, list):
            raise ValueError("variables must be given as elements of list.")
        
        self.variables = variables

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

        print(self.variables)
        X = X.drop(columns = self.variables)


        return X

class ElectricityBooleansToOrdinal(BaseEstimator, TransformerMixin):
    def __init__(self, variables: List[str]) -> None:
        if not isinstance(variables, list):
            raise ValueError("variables must be given as elements of list.")
        
        self.variables = variables

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

        print(self.variables)
        
        electricity_values = []

        # Assign values
        for i, row in X.iterrows():
            if row['noelec'] == 1:
                electricity_values.append(0)
            elif row['coopele'] == 1:
                electricity_values.append(1)
            elif row['public'] == 1:
                electricity_values.append(2)
            elif row['planpri'] == 1:
                electricity_values.append(3)
            else:
                electricity_values.append(np.nan)

        X['electricity_ordinal'] = electricity_values


        return X




######################## FEATURE ENGINEERING ###########################
########################################################################

'''
Data must be aggregate to household level.
Variables must be sorted into individual-level and household-level variables.

'''

