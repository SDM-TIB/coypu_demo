import multiprocessing as mp
import joblib as jb
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map
from sqlalchemy import create_engine
from sqlalchemy import engine as eng
import pandas as pd

class FastArrayProcessing():
    def __init__(self, func, array):
        self.n_workers = 2 * mp.cpu_count()
        self.func = func
        self.array = array
            
    def get_no_workers(self):
        return self.n_workers
    
    def set_no_workers(self, n):
        if n <= 2 * mp.cpu_count():
            self.n_workers = n
        print('No of workers more than 2*cpu_count, can not be set')
    
    def do_multiprocessing(self):
        p = mp.Pool(self.n_workers)
        return p.map(self.func, tqdm(self.array))
    
    def do_parallel_processing(self):
        result = jb.Parallel(n_jobs=self.n_workers, backend="multiprocessing")\
                 (jb.delayed(self.func)(value) for value in tqdm(self.array))
        return result
    
    def proc_batch(self, batch):
            return [self.func(value) for value in batch]
        
    def do_batch_processing(self):
        file_len = len(self.array)
        batch_size = round(file_len/self.n_workers)
        batches = [self.array[ix:ix+batch_size] for ix in tqdm(range(0, file_len, batch_size))]
        batch_outputs = jb.Parallel(self.n_workers, backend="multiprocessing")\
                       (jb.delayed(self.proc_batch)(batch) for batch in tqdm(batches))
        return [value for batch_output in batch_outputs for value in batch_output]
    
    def do_concurrent(self):
        batch_size = round(len(self.array)/self.n_workers)
        return process_map(self.func, self.array, max_workers=self.n_workers, chunksize=batch_size)
    

class DBCON():
    def __init__(self, host, port, uname, pwd, dbname):
        self._host = host
        self._port = port
        self._uname = uname
        self._pwd = pwd
        self._dbname = dbname
        
    def create_con(self):
        engine = create_engine(
        "mysql+pymysql://{user}:{pw}@{hostname}:{portno}/{db}".format(
            hostname=self._host, db=self._dbname, user=self._uname, pw=self._pwd, portno=self._port
        ),)
        self = engine.connect()
        
    def close_con(self):
        self.dbcon.close()
        
    def __enter__(self):
        engine = create_engine(
        "mysql+pymysql://{user}:{pw}@{hostname}:{portno}/{db}".format(
            hostname=self._host, db=self._dbname, user=self._uname, pw=self._pwd, portno=self._port
        ),)
        self.dbcon = engine.connect()
        return self
    
    def __exit__(self, type, value, traceback):
        if all((type, value, traceback)):
            raise (type, value, traceback)
        self.dbcon.close()
        return True
    
    def get_mysql_con(self):
        return self.dbcon
    

def main():
    pass

if __name__ == "__main__":
    main()
    

        
            
        
    
    
    
    
    
    
    
    
    
        
    
    
    