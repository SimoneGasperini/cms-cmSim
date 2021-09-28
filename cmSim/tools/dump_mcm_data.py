import os
import math
import time
import json
import pandas as pd

from functools import reduce
from cmSim.tools.mcm_rest import McM
from cmSim.tools.zipping import dump_zipped_json


def read_df_chunks(inputfile, chunksize):
    df = pd.read_parquet(inputfile)
    totsize = len(df.index)
    num = math.ceil(totsize / chunksize)
    df_chunks = [df[chunksize*i:chunksize*(i+1)] for i in range(num)]
    return df_chunks


def write_json_parts(df_chunks, dirpath, idx_start=0):
    num = len(df_chunks)
    digs = len(str(num))
    for idx in range(idx_start, num):
        print(f'\nProcessing chunk {idx+1} of {num}...')
        t1 = time.time()
        mcm = McM()
        results = {d_dataset: mcm.get_by_dataset_name(d_dataset)
                   for d_dataset in df_chunks[idx]['d_dataset']}
        prog = '0' * (digs - len(str(idx))) + str(idx)
        with open(f'{dirpath}{prog}_PART.json', mode='w') as file:
            json.dump(results, file, indent=4)
        t2 = time.time()
        elapsed = time.strftime('%H:%M:%S', time.gmtime(t2-t1))
        print(f'Elapsed time to process {len(df_chunks[idx])} rows: {elapsed}')


def write_json_full(outputfile, tempdir, zipped=False):
    dicts = []
    for filename in sorted(os.listdir(tempdir)):
        with open(tempdir+filename, mode='r') as file:
            dicts.append(json.load(file))
    data = reduce(lambda d1, d2: {**d1, **d2}, dicts)
    if zipped:
        dump_zipped_json(data, outputfile)
    else:
        with open(outputfile, mode='w') as file:
            json.dump(data, file, indent=4)


if __name__ == '__main__':

    dir = './../../data/'
    tempdir = dir + 'temp/'
    inputfile = dir + 'dataset_size_info.parquet'
    outputfile = dir + 'zip_mcm_dump.json'

    df_chunks = read_df_chunks(inputfile, chunksize=4000)
    if not os.path.exists(tempdir):
        os.makedirs(tempdir)
    write_json_parts(df_chunks, dirpath=tempdir)
    write_json_full(outputfile, tempdir=tempdir, zipped=True)
