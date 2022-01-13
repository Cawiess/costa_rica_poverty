from model import __version__ as _version
from model.config.config import config
from model.processing.data_manager import DataManager
import pytest

def test_processed_household_target_match():
    # Given
    #raw_data = DataManager.load_csv(file_name=config.package_config.raw_data)
    processed_data = DataManager.load_processed_excel(file_name=f"{config.package_config.processed_data}")

    #f"{config.package_config.processed_data}_v_{_version}"
    #f"{config.OUTPUT_DIR}/{file_name}_v_{_version}_{config.TODAY}.xlsx")
    
    householdTargetsMatching = (processed_data.groupby('idhogar')['target'].nunique()==1).reset_index()
    
    # When
    householdTargetMisMatch = householdTargetsMatching[householdTargetsMatching['target']==False]

    #if householdTargetMisMatch.shape[0]!=0:
    #    processed_data[processed_data['idhogar'].isin(householdTargetMisMatch['idhogar'])][['idhogar', 'Id', 'parentesco1', 'target']].to_excel('./logs/data_test_artifacts/test_household_target_match.xlsx')

    # Then
    assert householdTargetMisMatch.shape[0]==0