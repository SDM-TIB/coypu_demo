from rdfizer import semantify
import argparse
import logging
import parser_config
import shlex, subprocess

from os.path import abspath
import sys
sys.path.insert(0, abspath('.'))

from functions import *

@timer
def load_data(*args, **kwargs):
    try:
        cmd_list = "wget {} -P {}".format(kwargs['file_url'], kwargs['path'])
        cmd_list1 = "unzip {}/{} -d {}".format(kwargs['path'], kwargs['file_url'].replace('https://dataverse.harvard.edu/api/access/datafile/', ''),\
                kwargs['path'])
        print(shlex.split(cmd_list))
        d_process = subprocess.run(shlex.split(cmd_list), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        u_process = subprocess.run(shlex.split(cmd_list1), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print(d_process.stderr, u_process.stderr)
        preprocess_data(kwargs['path']+kwargs['file_url'].replace('https://dataverse.harvard.edu/api/access/datafile/', ''))
    except Exception as e:
        print("Error: ", e)
    
@timer   
def preprocess_data(*args, **kwargs):
    try:
        pass
    except Exception as e:
        print("Error: ", e)

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
            load_data(file_url='https://dataverse.harvard.edu/api/access/datafile/6898256', path=args.load_path)
            
        if args.preproc_data:
            print('Preprocessing data .........\n\n')
            preprocess_data()
        
        if args.config_file:
            print('Creating rdf data .........\n\n')
            semantify_data(args.config_file)
            
        if args.upload_data:
            print('Uploading data ..........\n\n')
            
    except Exception as e:
        print("Error: ", e)
    
if __name__ == "__main__":
    main()