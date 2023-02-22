import argparse
import logging

logger = logging.getLogger(__name__)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--load_data', type=bool, action=argparse.BooleanOptionalAction, help='load_data from source')
    parser.add_argument('--preproc_data', type=bool, action=argparse.BooleanOptionalAction, help='preprocess data or prepare data')
    parser.add_argument('--config_file', type=str, default=None, help='provide config file for semantifying data (e.g. config.ini)')
    parser.add_argument('--upload_data', type=str, default=None, help='provide upload location of data (e.g. tib, skynet etc.)')
    return parser.parse_args()
    
