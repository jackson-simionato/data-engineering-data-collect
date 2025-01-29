from datetime import datetime
import pandas as pd
import json
from pathlib import Path

class DataExporter:
    def __init__(self):
        self.datetime_now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')

    def __create_filename(self, filename, extension: str):
        folder = f'tabnews/dados/{extension}'
        Path(folder).mkdir(parents=True, exist_ok=True)

        return f'{folder}/{filename}_{self.datetime_now}.{extension}'

    def __export_to_csv(self, df: pd.DataFrame, filename: str):
        assert isinstance(df, pd.DataFrame), 'df must be a pandas DataFrame'

        filename = self.__create_filename(filename, 'csv')
        df.to_csv(filename, index=False)

        print(f'Data exported to {filename}')

    def __export_to_json(self, data: dict, filename: str):
        assert isinstance(data, (dict, list)), 'data must be a dictionary or list'
        if isinstance(data, list):
            assert all(isinstance(item, dict) for item in data), 'all items in list must be dictionaries'

        filename = self.__create_filename(filename, 'json')

        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

        print(f'Data exported to {filename}')

    def __export_to_parquet(self, df: pd.DataFrame, filename: str):
        assert isinstance(df, pd.DataFrame), 'df must be a pandas DataFrame'

        filename = self.__create_filename(filename, 'parquet')
        df.to_parquet(filename, index=False)

        print(f'Data exported to {filename}')

    def export_data(self, data, filename, type):
        if type == 'csv':
            data = pd.DataFrame(data)
            self.__export_to_csv(data, filename)
        elif type == 'json':
            self.__export_to_json(data, filename)
        elif type == 'parquet':
            data = pd.DataFrame(data)
            self.__export_to_parquet(data, filename)
        else:
            raise ValueError('Invalid type. Must be csv or json')
        

