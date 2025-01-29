from tabnews_api_types import GetContentParams
from tabnews_requester import TabNewsRequester
from data_exporter import DataExporter
import pandas as pd
from datetime import datetime, timedelta
import time

def get_content_last_hours(delta_hours:int, format:str = 'json'):
    page = 1
    stop_time = datetime.now() + timedelta(hours=delta_hours)
    keepsearching = True

    while keepsearching:
        print(page)

        params = GetContentParams(strategy='new', page=page, per_page=50)
        response = TabNewsRequester().get_content(params=params)

        if response.status_code == 200:                                            
            data = response.json()

            if not data:
                break


            last_date = data[-1]['created_at']
            last_date = datetime.strptime(last_date, '%Y-%m-%dT%H:%M:%S.%fZ')

            if last_date < stop_time:
                data = [dict_data for dict_data in data if datetime.strptime(dict_data['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ') >= stop_time]
                keepsearching = False

            DataExporter().export_data(data=data, filename='tabnews_get_contents', type=format)

            page += 1
            time.sleep(2)
        else:
            time.sleep(30)

    
if __name__ == '__main__':
    delta_hours = -5
    get_content_last_hours(delta_hours, format='parquet')