from tabnews_api_types import GetContentParams
from tabnews_requester import TabNewsRequester
from data_exporter import DataExporter
import pandas as pd
    
if __name__ == '__main__':
    params = GetContentParams(strategy='relevant', page=1, per_page=2)
    response = TabNewsRequester().get_content(params=params)
    data = response.json()
    df = pd.DataFrame(data)

    DataExporter().export_data(data=df, filename='tabnews_get_contents', type='csv')
    DataExporter().export_data(data=df, filename='tabnews_get_contents', type='parquet')
    DataExporter().export_data(data=data, filename='tabnews_get_contents', type='json')
