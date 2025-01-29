from tabnews_api_types import GetContentParams
from tabnews_requester import TabNewsRequester
import pandas as pd
    
if __name__ == '__main__':
    params = GetContentParams(strategy='relevant', page=1, per_page=2)
    response = TabNewsRequester().get_content(params=params)
    data = response.json()
    df = pd.DataFrame(data)
    print(df.head())
