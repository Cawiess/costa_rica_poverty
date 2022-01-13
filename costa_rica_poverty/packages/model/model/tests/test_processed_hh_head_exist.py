from model import __version__ as _version
from model.config.config import config
from model.processing.data_manager import DataManager

import pytest
import os

#@pytest.mark.skipif(len(os.listdir(config.OUTPUT_DIR))>1, reason="processed data exists")
def test_head_of_household_exists():
    # Given
    processed_data = DataManager.load_processed_excel(file_name=f"{config.package_config.processed_data}")
    
    # When
    hh_head = processed_data.groupby('idhogar')['parentesco1'].sum().reset_index()
    hh_head_none = hh_head[hh_head['parentesco1']!=1]
    
    # Then
    assert hh_head_none.shape[0]==0