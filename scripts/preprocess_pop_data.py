import os
import json
import pandas as pd
from tqdm import tqdm
from cmSim import utils

import warnings
warnings.filterwarnings('ignore')


def create_pop_directories(datatier_to_outdir):
    print('\nCreating popularity directories...', end='')
    for dt in datatier_to_outdir:
        dir = datatier_to_outdir[dt]
        if not os.path.exists(dir):
            os.makedirs(dir)
    print(' Done')


# Data Bookkeeping Service
def create_dbs_features_json(dbs_file, datatier_to_outdir):
    df = pd.read_parquet(dbs_file)
    df.dropna(inplace=True)
    df = df[(df['dsize'] > 0.) & (df['nfiles'] > 0) & (df['devts'] > 0)]
    for datatier in datatier_to_outdir:
        message = f'\nCreating "{datatier}/dbs_features.json" file...'
        print(message, flush=True)
        dframe = df[df['tier'] == datatier.upper()]
        data = {row['d_dataset']: {'tot_size': round(row['dsize']),
                                   'avg_file_size': round(row['dsize'] / row['nfiles']),
                                   'avg_event_size': round(row['dsize'] / row['devts'])}
                for _, row in tqdm(dframe.iterrows())}
        outfile = datatier_to_outdir[datatier] + 'dbs_features.json'
        with open(outfile, mode='w') as f:
            json.dump(data, f, indent=2)


# Monte Carlo Management
def create_mcm_features_json(datatier_to_mcm_file, datatier_to_outdir):
    pags = set(utils.get_pags())
    for datatier in datatier_to_mcm_file:
        message = f'\nCreating "{datatier}/mcm_features.json" file...'
        print(message, flush=True)
        infile = datatier_to_mcm_file[datatier]
        mcm_data = {}
        data = {}
        mcm_data = utils.get_mcm_data(filepath=infile)
        for dataset in tqdm(mcm_data):
            pwg = utils.get_pwg_from_dataset(dataset, mcm_data)
            campaign = utils.get_campaign_from_dataset(dataset, mcm_data)
            generator = utils.get_generator_from_dataset(dataset, mcm_data)
            if pwg != 'None' and campaign != 'None' and generator != 'None':
                data[dataset] = {}
                data[dataset]['pag'] = pwg if pwg in pags else 'Other PWG'
                data[dataset]['campaign'] = campaign
                data[dataset]['generator'] = generator
        outfile = datatier_to_outdir[datatier] + 'mcm_features.json'
        with open(outfile, mode='w') as f:
            json.dump(data, f, indent=2)


def get_datasets_names(datatier):
    mcm_features_file = f'./../data/popularity/{datatier}/mcm_features.json'
    dbs_features_file = f'./../data/popularity/{datatier}/dbs_features.json'
    with open(mcm_features_file, mode='r') as f:
        mcm_datasets_names = set(
            d for d in json.load(f) if d.endswith(datatier.upper()))
    with open(dbs_features_file, mode='r') as f:
        dbs_datasets_names = set(
            d for d in json.load(f) if d.endswith(datatier.upper()))
    df1 = pd.read_parquet('./../data/parquet/dataset_site_info.parquet')
    df1 = df1.drop(
        columns=['dataset_id', 'replica_time_create', 'br_user_group_id']).dropna()
    rep_datasets_names = set(
        df1[df1['tier'] == datatier.upper()]['dataset_name'])
    df2 = pd.read_parquet('./../data/parquet/dataset_reads.parquet').dropna()
    df2['tier'] = df2['d_dataset'].apply(lambda name: name.split('/')[-1])
    acc_datasets_names = set(
        df2[df2['tier'] == datatier.upper()]['d_dataset'])
    datasets_names = set.intersection(mcm_datasets_names, dbs_datasets_names,
                                      rep_datasets_names, acc_datasets_names)
    return datasets_names


# Datasets replicas on T1/T2 disk
def create_replicas_info_json(replicas_file, datatier_to_outdir):
    replicas_df = pd.read_parquet(replicas_file)
    replicas_df = replicas_df.drop(
        columns=['dataset_id', 'replica_time_create', 'br_user_group_id', 'tier']).dropna()
    for datatier in datatier_to_outdir:
        message = f'\nCreating "{datatier}/replicas_info.json" file...'
        print(message, flush=True)
        datasets_names = get_datasets_names(datatier=datatier.upper())
        dframe = replicas_df[replicas_df['dataset_name'].isin(datasets_names)]
        for col in ['min_time', 'max_time']:
            dframe[col] = dframe[col].apply(utils.get_int_from_date)
        data = {}
        for d, df in tqdm(dframe.groupby('dataset_name')):
            data[d] = {'num_replicas': {},
                       'size_replicas': {},
                       'num_sites_replicas': {}}
            start = utils.get_date_from_int(df['min_time'].min())
            end = utils.get_date_from_int(df['max_time'].max())
            date_range = [utils.get_int_from_date(dt.date())
                          for dt in pd.date_range(start=start, end=end, freq='D')]
            for date in date_range:
                df_date = df[(df['min_time'] <= date) &
                             (date <= df['max_time'])]
                num_replicas = len(df_date)
                if num_replicas > 0:
                    size_replicas = round(df_date['rep_size'].sum())
                    num_sites_replicas = df_date['node_name'].nunique()
                    data[d][f'num_replicas'][date] = num_replicas
                    data[d][f'size_replicas'][date] = size_replicas
                    data[d][f'num_sites_replicas'][date] = num_sites_replicas
        outfile = datatier_to_outdir[datatier] + 'replicas_info.json'
        with open(outfile, mode='w') as f:
            json.dump(data, f)


# Datasets reads/accesses
def create_accesses_info_json(accesses_file, datatier_to_outdir):
    accesses_df = pd.read_parquet(accesses_file).dropna()
    accesses_df['tier'] = accesses_df['d_dataset'].apply(
        lambda name: name.split('/')[-1])
    for datatier in datatier_to_outdir:
        message = f'\nCreating "{datatier}/accesses_info.json" file...'
        print(message, flush=True)
        datasets_names = get_datasets_names(datatier=datatier.upper())
        dframe = accesses_df[accesses_df['d_dataset'].isin(datasets_names)]
        data = {d: {'num_accesses': {int(row['day'][2:]): utils.get_rounded_num_accesses(row['fract_read'])
                                     for _, row in df.iterrows()}}
                for d, df in tqdm(dframe.groupby('d_dataset'))}
        outfile = datatier_to_outdir[datatier] + 'accesses_info.json'
        with open(outfile, mode='w') as f:
            json.dump(data, f, indent=2)


def create_pop_dataframe_parquet(datatier_to_outdir):
    for datatier in datatier_to_outdir:
        message = f'\nCreating "{datatier}/pop_dataframe.parquet" file...'
        print(message, end='')
        key_to_file = {'dbs': f'./../data/popularity/{datatier}/dbs_features.json',
                       'mcm': f'./../data/popularity/{datatier}/mcm_features.json',
                       'rep':  f'./../data/popularity/{datatier}/replicas_info.json',
                       'acc': f'./../data/popularity/{datatier}/accesses_info.json'}
        key_to_data = {}
        for key in key_to_file:
            with open(key_to_file[key], mode='r') as file:
                key_to_data[key] = json.load(file)
        datasets_names = list(key_to_data['rep'].keys())
        dataset_to_index = {dataset: index
                            for index, dataset in enumerate(datasets_names)}
        dict = {dataset_to_index[dataset]: {'dataset_name': dataset}
                for dataset in datasets_names}
        for dataset in datasets_names:
            index = dataset_to_index[dataset]
            for key in key_to_file:
                for info in key_to_data[key][dataset]:
                    dict[index][info] = key_to_data[key][dataset][info]
        df = pd.DataFrame.from_dict(dict, orient='index')
        outfile = datatier_to_outdir[datatier] + 'pop_dataframe.parquet'
        df.to_parquet(path=outfile)
        fix_pop_dataframe_parquet(path=outfile)
        print(' Done')


def fix_pop_dataframe_parquet(path):
    df = pd.read_parquet(path)
    for col in ['num_replicas', 'size_replicas', 'num_sites_replicas', 'num_accesses']:
        df[col] = df[col].apply(lambda dict: {k: int(dict[k]) if dict[k] is not None else 0
                                              for k in dict})
    df['size_replicas'] = df.apply(lambda row: {day: row['size_replicas'][day] / row['tot_size']
                                                for day in row['size_replicas']}, axis=1)
    df.rename(columns={'size_replicas': 'fract_replicas'}, inplace=True)
    df.to_parquet(path)


if __name__ == '__main__':

    datatiers = ['aodsim', 'miniaodsim', 'nanoaodsim']
    dbs_file = './../data/parquet/dataset_size_info.parquet'
    datatier_to_mcm_file = {
        dt: f'./../data/mcm/{dt}_mcm_data.json' for dt in datatiers}
    replicas_file = './../data/parquet/dataset_site_info.parquet'
    accesses_file = './../data/parquet/dataset_reads.parquet'
    datatier_to_outdir = {
        dt: f'./../data/popularity/{dt}/' for dt in datatiers}

    create_pop_directories(datatier_to_outdir)
    create_dbs_features_json(dbs_file, datatier_to_outdir)
    create_mcm_features_json(datatier_to_mcm_file, datatier_to_outdir)
    create_replicas_info_json(replicas_file, datatier_to_outdir)
    create_accesses_info_json(accesses_file, datatier_to_outdir)
    create_pop_dataframe_parquet(datatier_to_outdir)
