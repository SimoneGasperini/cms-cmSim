import os
import math
import time
import pandas as pd
from cmSim.tools.mcm_rest import McM


def read_df_chunks(inputfile, chunksize=4000):
    df = pd.read_parquet(inputfile)
    totsize = len(df.index)
    num = math.ceil(totsize / chunksize)
    df_chunks = [df[chunksize*i:chunksize*(i+1)] for i in range(num)]
    return df_chunks


def query_mcm(d_dataset, mcm):
    results = mcm.get_by_dataset_name(d_dataset)
    pwg = results.get('pwg', 'None')
    campaign = results.get('member_of_campaign', 'None')
    return pd.Series([pwg, campaign])


def write_part(df, dirpath, idx, digs):
    mcm = McM()
    df[['pwg', 'campaign']] = df['d_dataset'].apply(query_mcm, mcm=mcm)
    prog = str(idx)
    prog = '0' * (digs - len(prog)) + prog
    df.to_parquet(f'{dirpath}{prog}_PART.parquet')


def write_parquet_parts(df_chunks, dirpath, idx_start=0):
    num = len(df_chunks)
    digs = len(str(num))
    for idx in range(idx_start, num):
        print(f'\nProcessing chunk {idx+1} of {num}...')
        t1 = time.time()
        write_part(df=df_chunks[idx], dirpath=dirpath, idx=idx, digs=digs)
        t2 = time.time()
        elapsed = time.strftime('%H:%M:%S', time.gmtime(t2-t1))
        print(f'Elapsed time to process {len(df_chunks[idx])} rows: {elapsed}')


def write_parquet_full(outputfile, tempdir):
    dataframes = [pd.read_parquet(tempdir + file)
                  for file in sorted(os.listdir(tempdir))]
    df = pd.concat(dataframes)
    df.to_parquet(outputfile)


if __name__ == '__main__':

    dir = './../../data/'
    tempdir = dir + 'temp/'
    inputfile = dir + 'dataset_size_info.parquet'
    outputfile = dir + 'dataset_size_info_complete.parquet'

    df_chunks = read_df_chunks(inputfile)
    if not os.path.exists(tempdir):
        os.makedirs(tempdir)
    write_parquet_parts(df_chunks, dirpath=tempdir)
    write_parquet_full(outputfile, tempdir=tempdir)
