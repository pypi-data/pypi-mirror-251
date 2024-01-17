import os
import pandas as pd

class DataReader:
    def __init__(self, data_folder='data'):
        self.data_folder = data_folder

    def get_data(self, file_name):
        file_path = os.path.join(self.data_folder, file_name)
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File {file_name} not found in {self.data_folder}")

        # CSVファイルを読み込んでDataFrameとして返す
        return pd.read_csv(file_path)
