from sklearn.pipeline import Pipeline
from model.config.config import config

from processing import preprocessors as pp


'''
This module contains the Sklearn pipelines which gathers the preprocessors and analyzers
into an ordered sequence of operations. These pipelines are then executed by the main.py module.
'''


### DATA PREPROCESSING
preprocessing_pipeline = Pipeline(
    [
        (
            "Normalize column labels",
            pp.ColumnLabelNormalizer()
        ),
        (
            "Normalize variable values",
            pp.ColumnValueNormalizer()
        ),
        (
            "Correcting head of household exists",
            pp.HeadOfHouseholdExistCorrection(variables=config.preprocessing_config.head_of_household_exist)
        ),
        (
            "Correcting poverty levels",
            pp.IntraHouseholdTargetCorrection(variables=config.preprocessing_config.intra_household_target_correction)
        ),
        (
            "Convert strings to numerical binary",
            pp.BinaryEncoder(variables=config.preprocessing_config.yes_no_map_to_numerical)
        ),
        (
            "Correcting missing values for number of tablets owned",
            pp.NumberOfTabletsMissingValues(variables=config.preprocessing_config.num_tablets_missing)
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