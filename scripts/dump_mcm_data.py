import os
import math
import time
import json
import pandas as pd

from cmSim.tools.mcm_rest import McM
from cmSim.tools.multithread import ThreadPool
from cmSim.tools.zipping import dump_zipped_json


def read_df_chunks(inputfile, datatier, chunksize):
    df = pd.read_parquet(inputfile)
    df = df[df['tier'] == datatier]
    totsize = len(df.index)
    num = math.ceil(totsize / chunksize)
    df_chunks = [df[chunksize*i:chunksize*(i+1)] for i in range(num)]
    return df_chunks


def query_mcm_system(datasets_names, num_threads=4):
    mcm = McM()
    thread_pool = ThreadPool(num_threads=num_threads)
    thread_pool.map(func=mcm.get_by_dataset_name,
                    sequence=datasets_names)
    result = thread_pool.get_result()
    return result


def write_json_parts(df_chunks, dirpath, idx_start=0):
    num = len(df_chunks)
    for idx in range(idx_start, num):
        print(f'\nProcessing chunk {idx+1} of {num}...')
        t1 = time.time()
        datasets_names = df_chunks[idx]['d_dataset'].tolist()
        result = query_mcm_system(datasets_names)
        prog = '0' * (len(str(num)) - len(str(idx))) + str(idx)
        with open(f'{dirpath}{prog}_PART.json', mode='w') as file:
            json.dump(result, file, indent=4)
        t2 = time.time()
        elapsed = time.strftime('%H:%M:%S', time.gmtime(t2-t1))
        print(f'Elapsed time to process {len(df_chunks[idx])} rows: {elapsed}')


def write_json_full(outputfile, tempdir, zipped=True):
    data = {}
    for filename in sorted(os.listdir(tempdir)):
        with open(tempdir+filename, mode='r') as file:
            curr = json.load(file)
            data = {**data, **curr}
    if zipped:
        dump_zipped_json(data, outputfile)
    else:
        with open(outputfile, mode='w') as file:
            json.dump(data, file, indent=4)


if __name__ == '__main__':

    tempdir = './../data/temp/'
    if not os.path.exists(tempdir):
        os.makedirs(tempdir)

    df_chunks = read_df_chunks(inputfile='./../data/dataset_size_info.parquet',
                               datatier='NANOAODSIM',
                               chunksize=4000)
    write_json_parts(df_chunks=df_chunks,
                     dirpath=tempdir,
                     idx_start=0)
    write_json_full(outputfile='./../data/nanoaodsim_mcm_data.json',
                    tempdir=tempdir,
                    zipped=True)
