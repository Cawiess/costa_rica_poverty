import pandas as pd

from model import __version__ as _version
from model.config.config import config
from model.config.logging import ProcessLogger
from model.processing.data_manager import DataManager
from model.pipelines import pipelines

ProcessLogger = ProcessLogger(__name__)

def main():
    ProcessLogger.processLogger.info(f" ======== Starting process with version: {_version} ========")

    raw_data = DataManager.load_csv(file_name=config.package_config.raw_data)

    ProcessLogger.processLogger.info(f"\n Raw data dimensions: \n num rows: {raw_data.shape[0]}, num cols: {raw_data.shape[1]}")
    ProcessLogger.processLogger.info(f"Primary dependent variable(s): {config.model_config.primary_dependent_variables}")
    ProcessLogger.processLogger.info(f"\n Preprocessing pipeline: \n {pipelines.preprocessing_pipeline}")
    
    processed_data = pipelines.preprocessing_pipeline.fit_transform(raw_data)
    ProcessLogger.processLogger.info(f"\n Processed data dimensions: \n num rows: {raw_data.shape[0]}, num cols: {raw_data.shape[1]}")

    DataManager.export_excel(data=processed_data, file_name=config.package_config.processed_data)


    return 0

if __name__=='__main__':
    main()
    ProcessLogger.processLogger.info(f" ========================== END ========================== ")