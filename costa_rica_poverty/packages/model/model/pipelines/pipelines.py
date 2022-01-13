from sklearn.pipeline import Pipeline
#TODO: Import preprocessors and analyzers needs setup of config files.

from processing import preprocessors as pp


'''
This module contains the Sklearn pipelines which gathers the preprocessors and analyzers
into an ordered sequence of operations. These pipelines are then executed by the main.py module.
'''


### DATA PREPROCESSING
preprocessing_pipeline = Pipeline(
    [
        (
            "Correcting poverty levels",
            pp.IntraHouseholdTargetCorrection()
        ),
        (
            "Correcting head of household exists",
            pp.HeadOfHouseholdExistCorrection()
        ),
        (
            "Preprocessing pipeline step One",
            pp.ColumnLabelNormalizer()
        ),
        (
            "Preprocessing pipeline Step Two",
            pp.ColumnValueNormalizer()
        )
    ]
)


### DATA FILTERING AND VARIABLE SELECTION
filtering_pipeline = Pipeline(
    [
        (
            "Filtering pipeline step One",
            print('Step one')
        ),
        (
            "Filtering pipeline Step Two",
            print('Step two')
        )
    ]
)