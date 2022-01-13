import pandas as pd

from model.config import config
from model import __version__ as _version


class DataManager:
    def load_csv(*, file_name: str) -> pd.DataFrame:
        _data = pd.read_csv(f"{config.INPUT_DIR}/data/{file_name}.csv")
        return _data

    def load_AWS():
        pass

    def load_KOBO():
        pass

    def export_excel(*, data: pd.DataFrame, file_name: str) -> None:
        #data.to_excel(f"{config.OUTPUT_DIR}/{file_name}_v_{_version}_{config.TODAY}.xlsx", index=False)
        data.to_excel(f"{config.OUTPUT_DIR}/{file_name}_v_{_version}.xlsx", index=False)
        return None

    def load_processed_excel(*, file_name: str) -> pd.DataFrame:
        _data = pd.read_excel(f"{config.OUTPUT_DIR}/{file_name}_v_{_version}.xlsx")
        return _data




