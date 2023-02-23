from rdfizer import semantify
import argparse
import logging
import parser_config

from os.path import abspath
import sys
sys.path.insert(0, abspath('.'))

from functions import *

@timer
def load_data(*args, **kwargs):
    try:
        pass
    except Exception as e:
        pass
    
@timer   
def preprocess_data(*args, **kwargs):
    try:
        pass
    except Exception as e:
        pass

@timer
def semantify_data(config_file, *args, **kwargs):
    try:
        semantify(config_file)
    except Exception as e:
        print('Error:', e)
    else:
        print('Successfully created RDF knowledge graph')
    finally:
        exit()


def main(*args, **kwargs):
    try:
        args = parser_config.parse_args()
        if args.load_data:
            print('Loading data ..........\n\n')
            
        if args.preproc_data:
            print('Preprocessing data .........\n\n')
        
        if args.config_file:
            print('Creating rdf data .........\n\n')
            semantify_data(args.config_file)
            
        if args.upload_data:
            print('Uploading data ..........\n\n')
            
    except Exception as e:
        print("Error: ", e)
    
if __name__ == "__main__":
    main()