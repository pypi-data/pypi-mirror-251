import requests
import pandas as pd 
from datetime import datetime




class Analysis:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        # self.curveid = curveid
        self.url = "https://ahmadriad.art/login/"
        self.token = self.get_token()

    def get_token(self):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        payload = {
            'username': self.username,
            'password': self.password
        }
        response = requests.post(self.url, headers=headers, data=payload)
        data = response.json()
        if response.status_code == 202:
            
            return data['access_token']
        else:
            raise ValueError(f"Authentication failed: {data['detail']}", response.status_code)

    def DefTable(self,curveid = None):
        if curveid is None:
            url_1 = 'https://ahmadriad.art/get/DefTable'
            headers_1 = {
                'accept': 'application/json',
                'Authorization': f"Bearer {self.token}"
            }
            response_1 = requests.get(url_1, headers=headers_1)
            
            if response_1.status_code == 200:
                data_1 = response_1.json()
                df = pd.DataFrame(data_1)
                return df
            else:
                raise ValueError(f"Failed to get table: {data_1['detail']}", response_1.status_code)
            
            
        else:
            url_1 = f'https://ahmadriad.art/get/DefTable?cur={curveid}'
            headers_1 = {
                'accept': 'application/json',
                'Authorization': f"Bearer {self.token}"
            }
            response_1 = requests.get(url_1, headers=headers_1)
            
            if response_1.status_code == 200:
                data_1 = response_1.json()
                df = pd.DataFrame(data_1)
                return df
            
            else:
                raise ValueError(f"Failed to get table: {data_1['detail']}", response_1.status_code)
    
            
    
            
    def TimeSeries(self, curveid = None, startdate = None, enddate = None):
        if curveid is None:
            if startdate is not None and enddate is not None:
                
                url_1= f'https://ahmadriad.art/get/TimeSeries?startdate={startdate}&enddate={enddate}'
                headers_1 = {
                    'accept': 'application/json',
                    'Authorization': f"Bearer {self.token}"
                }
                        
                response_1 = requests.get(url_1, headers=headers_1)
                if response_1.status_code == 200:
                    data_1 = response_1.json()
                    df = pd.DataFrame(data_1)
                    return df
                else:
                    raise ValueError(f"Failed to get table: {data_1['detail']}", response_1.status_code)
                    
                    
            elif startdate is not None and enddate == None:
                url_1= f'https://ahmadriad.art/get/TimeSeries?startdate={startdate}'
                headers_1 = {
                    'accept': 'application/json',
                    'Authorization': f"Bearer {self.token}"
                }
                        
                response_1 = requests.get(url_1, headers=headers_1)
                if response_1.status_code == 200:
                    data_1 = response_1.json()
                    df = pd.DataFrame(data_1)
                    return df
                else:
                    raise ValueError(f"Failed to get table: {data_1['detail']}", response_1.status_code)
                    
            else:
                url_1= 'https://ahmadriad.art/get/TimeSeries'
                headers_1 = {
                    'accept': 'application/json',
                    'Authorization': f"Bearer {self.token}"
                }
                        
                response_1 = requests.get(url_1, headers=headers_1)
                if response_1.status_code == 200:
                    data_1 = response_1.json()
                    df = pd.DataFrame(data_1)
                    return df
                else:
                    raise ValueError(f"Failed to get table: {data_1['detail']}", response_1.status_code)
            
                
            
                
        else:
            if startdate is not None and enddate is not None:
                
                url_1= f'https://ahmadriad.art/get/TimeSeries?cur={curveid}&startdate={startdate}&enddate={enddate}'
                headers_1 = {
                    'accept': 'application/json',
                    'Authorization': f"Bearer {self.token}"
                }
                        
                response_1 = requests.get(url_1, headers=headers_1)
                if response_1.status_code == 200:
                    data_1 = response_1.json()
                    df = pd.DataFrame(data_1)
                    return df
                else:
                    raise ValueError(f"Failed to get table: {data_1['detail']}", response_1.status_code)
                    
                    
            elif startdate is not None and enddate == None:
                url_1= f'https://ahmadriad.art/get/cur={curveid}&TimeSeries?startdate={startdate}'
                headers_1 = {
                    'accept': 'application/json',
                    'Authorization': f"Bearer {self.token}"
                }
                        
                response_1 = requests.get(url_1, headers=headers_1)
                if response_1.status_code == 200:
                    data_1 = response_1.json()
                    df = pd.DataFrame(data_1)
                    return df
                else:
                    raise ValueError(f"Failed to get table: {data_1['detail']}", response_1.status_code)
                    
            else:
                url_1= f'https://ahmadriad.art/get/TimeSeries?cur={curveid}'
                headers_1 = {
                    'accept': 'application/json',
                    'Authorization': f"Bearer {self.token}"
                }
                        
                response_1 = requests.get(url_1, headers=headers_1)
                
                if response_1.status_code == 200:
                    data_1 = response_1.json()
                    df = pd.DataFrame(data_1)
                    return df
                else:
                    raise ValueError(f"Failed to get table: {data_1['detail']}", response_1.status_code)
            
            
        # table['ValueDate']= pd.to_datetime(table['ValueDate'])
        # startdate= pd.to_datetime(startdate)
        # enddate= pd.to_datetime(enddate)
        # if startdate is not None and enddate is not None:
        #     sliced_by_date_range = table[(table['ValueDate'] >= startdate) & (table['ValueDate'] <= enddate)]
        #     return sliced_by_date_range
        
        # elif startdate is not None and enddate == None:
        #     sliced_by_date_range = table[(table['ValueDate'] >= startdate)]
        #     return sliced_by_date_range
        
        # else:
        #     return table
  
    
#%%%%%%%%%%%      
# curveid=2
# analysis = Analysis('ahmadriad2@gmail.com', '12345678')


# table = analysis.DefTable((2,4,66,8,9,0,88))
# table_1= analysis.TimeSeries()

#%%%%%%%%%%%

        
    

    
    
    









































