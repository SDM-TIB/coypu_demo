from random import random
import pandas as pd
import requests
import base64
import time
import functools
from os.path import join
import json
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import numpy as np

def replace(self, updated_file: str, replace: dict = {'\'': ''},
            header: bool = False, index=False):
    df = pd.read_csv(self.file_inpath, encoding='utf-8')
    df.replace(replace, regex=True, inplace=True)
    df.to_csv(updated_file, index=index, header=header)
    print('preview data after removig quotes')
    print(df.head(2))
    del df


def get_sample_data(self, updated_file: str, sample_rows: int = 20000,
                    chunksize: int = 100000, random_state: int = 1,
                    index: bool = False):
    chunks = pd.read_csv(self.file_inpath, chunksize=chunksize,
                         encoding='utf-8', low_memory=False)
    for chunk in chunks:
        df = chunk.sample(sample_rows, random_state=random_state)
        break
    df.to_csv(updated_file, index=index)
    del df

def auth(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if args[0].auth_type =='oauth':
            #url = args[0].url + "/auth/realms/cmem/protocol/openid-connect/token"
            url = "https://pm.coypu.org/auth/realms/cmem/protocol/openid-connect/token"
            payload = 'grant_type=client_credentials&client_id={}&client_secret={}'\
                .format(args[0].id_or_user, args[0].pass_or_secret)
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            response = requests.request("POST", url, headers=headers, data=payload)
            if response.status_code == 200:
                args[0].auth = 'Bearer ' + response.json()['access_token']
                args[0].url = args[0].url + "/dataplatform/proxy/default/sparql"
        elif args[0].auth_type =='basic':
            usr_pass = args[0].id_or_user + ':' + args[0].pass_or_secret
            args[0].auth =  "Basic {}".format(base64.b64encode(usr_pass.encode()).decode())
        return func(*args, **kwargs)
    return wrapper

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        time_pre = time.time()
        ret = func(*args, **kwargs)
        print('Total time taken by {} function: {}'.format(func.__name__,time.time()-time_pre))
        return ret
    return wrapper

@timer
def json_to_csv(json, save_path, filename, columns=None, ret=False):
    df = pd.json_normalize(json)
    # print(df.columns)
    print(df.memory_usage())
    print(df.info(memory_usage=True))
    df.to_csv(join(save_path, filename+'.csv'), encoding='utf-8', columns=columns, index=False)
    if ret:
        return df[columns]
    
@timer
def dictfrmjson(filename):
    with open(filename, 'r') as f:
        d = json.load(f)
    return dict(d)

def get_public_data_info(name:str, url:str):
    API_URL = url + "package_list"
    try:
        response = requests.get(API_URL)
    except requests.exceptions.RequestException as e:
        print("ERROR ACCESSING API: ", API_URL, e.__str__())
    datasets = response.json().get('result')
    dataset_list = [id for id in datasets if name in id]
    
    API_URL = url + "package_show"
    for id in dataset_list:
        try:
            response = requests.get(API_URL, params = {"id": id})
        except requests.exceptions.RequestException as e:
            print("ERROR ACCESSING API: ", API_URL, e.__str__())
        print (id, response.json().get('result'))
    

def create_dataset(dataset_dict:dict, url:str, user_token):
    API_URL = url + "package_create"
    try:
        response = requests.post(API_URL, data = dataset_dict, headers={'Authorization': user_token})
    except requests.exceptions.RequestException as e:
        print("ERROR ACCESSING API: ", API_URL, e.__str__())
    return response.json()


def worldbank_layout(df, app):
    app.layout = html.Div([
        html.Div([

            html.Div([
                dcc.Dropdown(
                    np.insert(df['Country Name'].unique(), 0, 'All Countries'),
                    'All Countries',
                    id='country-name',
                    multi=True,
                    searchable=True,
                ),
            ], style={'width': '30%', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    df['Indicator Name'].unique(),
                    'Fertility rate, total (births per woman)',
                    id='xaxis-column'
                ),
                dcc.RadioItems(
                    ['Linear', 'Log'],
                    'Linear',
                    id='xaxis-type',
                    inline=True
                )
            ], style={'width': '30%', 'display': 'inline-block'}),


            html.Div([
                dcc.Dropdown(
                    df['Indicator Name'].unique(),
                    'Life expectancy at birth, total (years)',
                    id='yaxis-column'
                ),
                dcc.RadioItems(
                    ['Linear', 'Log'],
                    'Linear',
                    id='yaxis-type',
                    inline=True
                )
            ], style={'width': '30%', 'display': 'inline-block'})
        ]),

        dcc.Graph(id='indicator-graphic'),

        dcc.RangeSlider(
            min=df['Year'].min(), 
            max=df['Year'].max(), 
            step=5, 
            value=[df['Year'].min()+10, df['Year'].max()-10], 
            id='year-range-slider',
            marks={str(year): str(year) for year in df['Year'].unique()},
        )
    ])
    return app


