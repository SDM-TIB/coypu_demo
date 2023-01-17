import requests
from credentials import *
from functions import *
import pandas as pd
from io import StringIO
print(__package__)
from os.path import join, abspath
from functools import reduce
from urllib.parse import urlencode, quote
from DeTrusty.Molecule.MTManager import ConfigFile
from DeTrusty import run_query



import sys
sys.path.insert(0, abspath('.'))

class SPARQLRequest():
    def __init__(self, url=None, id_or_user=None, pass_or_secret=None,\
                 auth_type:str=None, is_fdq=False, is_fdq_serive=False):
        self.id_or_user = id_or_user
        self.pass_or_secret = pass_or_secret
        self.auth_type = auth_type
        self.auth = None
        self.url = url
        self.is_fdq = is_fdq
        self.is_fdq_serive = is_fdq_serive
                   
    @auth
    def __set_params(self, accept_type='text/csv', *args, **kwargs):
        if self.auth_type:
            self.headers = {'Content-Type': 'application/sparql-query', 'Accept': accept_type,
                       'Authorization':self.auth}
        elif self.is_fdq:
            self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        else:
            self.headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Accept': accept_type}
        
    def __set_query(self, query):
        if self.is_fdq and self.is_service:
                self.query="query="+query+"&sparql1_1=True"
        elif self.is_fdq:
                self.query="""query="""+query
        elif self.auth_type:
            self.query=query
        else:
            self.query='default-graph-uri=&query={}'.format(quote(query))
        
    @timer                    
    def execute(self, query, config=None, join_stars_locally=None):
        # print(self.headers, self.query)
        self.config = config
        try:
            if self.is_fdq and config:
                # print('FDQ')
                self.response = run_query(query, config=config, join_stars_locally=join_stars_locally)
            else:
                # print('Non-FDQ')
                self.__set_params()
                self.__set_query(query)
                response = requests.request("POST", self.url, headers=self.headers, data=self.query, stream=True)
                if response.status_code == 200:
                    print("Passed Query Status: {}".format(response.status_code))
                    self.response = response
                else:
                    print("Failed Query: {}".format(response.content))
        except Exception as e:
            print("Failed Query: {}".format(str(e)))
    
            
    @timer
    def save(self, save_path, filename:str):
        try:
            if self.is_fdq and self.config:
                json_to_csv(self.response['results']['bindings'], save_path, \
                    filename, columns=[var+'.value' for var in self.response['head']['vars']])
            elif self.response.headers['Content-Type']=='text/csv':
                with open(join(save_path, filename+'.csv'), 'wb') as fd:
                    for chunk in self.response.iter_content(chunk_size=128):
                        fd.write(chunk)
            elif self.response.headers['Content-Type']=='application/json':
                with open(join(save_path, filename+'.json'), 'wb') as fd:
                    for chunk in self.response.iter_content(chunk_size=128):
                        fd.write(chunk)
                json_to_csv(self.response.json()['results']['bindings'], save_path, \
                    filename, columns=[var+'.value' for var in self.response.json()['head']['vars']])
            else:
                raise TypeError("Unknown response content-type")
           
        except Exception as e: 
            print("Failed Save: {}".format(str(e)))           
        
        del self.response
        


if __name__ == "__main__":
    
    query = """PREFIX  rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT DISTINCT ?s ?o WHERE{?s a ?o.} LIMIT 10"""

    cmemc_query = SPARQLRequest(client_url_imp, client_id_imp, client_secret_imp, 'oauth')
    print(cmemc_query.execute(query))
    print(cmemc_query.response.content)
    
    
    """fuseki_query = SPARQLRequest(fuseki_endpoint_infai, fuseki_user_infai, fuseki_pw_infai, 'basic')
    print(fuseki_query.execute(query))
    print(fuseki_query.response.content)"""
    
    fuseki_query = SPARQLRequest(skynet_endpoint, skynet_user, skynet_pass, 'basic')
    print(fuseki_query.execute(query))
    print(fuseki_query.response.content)