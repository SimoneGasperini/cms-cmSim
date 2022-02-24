import os
import json
import numpy as np
import pandas as pd
from tqdm import tqdm
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from cmSim import utils

tqdm.pandas()
sim_tiers = ['AODSIM', 'MINIAODSIM', 'NANOAODSIM']


def create_datasets_list_sim_parquet():
    print(f'Creating "datasets_list_sim.parquet"...', flush=True, end='')
    df = pd.read_parquet(
        './../data/parquet/dataset_size_info.parquet').dropna()
    df = df[df['dsize'] > 0.]
    df = df[df['nfiles'] > 0]
    df = df[df['devts'] > 0]
    df = df[df['tier'].isin(sim_tiers)]
    df.reset_index(drop=True).to_parquet('./../data/datasets_list_sim.parquet')
    print(' Done')


def create_data_replicas_sim_parquet():
    print(f'Creating "data_replicas_sim.parquet"...', flush=True, end='')
    df = pd.read_parquet('./../data/parquet/dataset_site_info.parquet')
    df = df.drop(
        columns=['dataset_id', 'replica_time_create', 'br_user_group_id']).dropna()
    df = df[df['tier'].isin(sim_tiers)]
    for col in ['min_time', 'max_time']:
        df[col] = df[col].apply(lambda date: date.strftime('%Y%m%d'))
    df.reset_index(drop=True).to_parquet('./../data/data_replicas_sim.parquet')
    print(' Done')


def create_data_accesses_sim_parquet():
    print(f'Creating "data_accesses_sim.parquet"...', flush=True, end='')
    df = pd.read_parquet('./../data/parquet/dataset_reads.parquet').dropna()
    df['tier'] = df['d_dataset'].apply(lambda name: name.split('/')[-1])
    df = df[df['tier'].isin(sim_tiers)]
    df['num_accesses'] = df['fract_read'].apply(utils.get_rounded_num_accesses)
    df.reset_index(drop=True).to_parquet('./../data/data_accesses_sim.parquet')
    print(' Done')


def create_datasets_mcm_info_json():
    for sim_tier in sim_tiers:
        filepath = f'./../data/mcm/{sim_tier.lower()}_mcm_data.json'
        mcm_data = utils.get_mcm_data(filepath)
        temp_data = {dataset: {'pwg': utils.get_pwg_from_dataset(dataset, mcm_data),
                               'campaign': utils.get_campaign_from_dataset(dataset, mcm_data),
                               'generator': utils.get_generator_from_dataset(dataset, mcm_data)}
                     for dataset in tqdm(mcm_data, desc=f'Getting {sim_tier} datasets info')}
        with open(f'./../data/{sim_tier.lower()}_temp.json', mode='w') as f:
            json.dump(temp_data, f)
        mcm_data = None
        temp_data = None
    print(f'Creating "datasets_mcm_info.json"...', flush=True, end='')
    data = {}
    for sim_tier in sim_tiers:
        filename = f'./../data/{sim_tier.lower()}_temp.json'
        with open(filename, mode='r') as f:
            data.update(json.load(f))
        os.remove(filename)
    with open(f'./../data/datasets_mcm_info.json', mode='w') as file:
        json.dump(data, file, indent=2)
    print(' Done')


def create_data_replicas_on_disk_json():
    print(f'Creating "data_replicas_on_disk.json"...', flush=True)
    df = pd.read_parquet('./../data/data_replicas_sim.parquet')
    data = {dataset: {} for dataset in set(df['dataset_name'])}
    for dataset, dframe in tqdm(df.groupby('dataset_name')):
        data[dataset]['intervals'] = set(
            zip(dframe['min_time'], dframe['max_time']))
        data[dataset]['months'] = set()
        for start, end in data[dataset]['intervals']:
            dt = datetime.strptime(start, '%Y%m%d').date()
            data[dataset]['months'].add(dt.strftime('%Y-%m'))
            while dt <= datetime.strptime(end, '%Y%m%d').date():
                dt += relativedelta(months=1)
                data[dataset]['months'].add(dt.strftime('%Y-%m'))
        data[dataset]['intervals'] = list(data[dataset]['intervals'])
        data[dataset]['months'] = sorted(list(data[dataset]['months']))
    with open('./../data/data_replicas_on_disk.json', mode='w') as file:
        json.dump(data, file, indent=2)


def filter(row, data):
    for t1, t2 in data[row['d_dataset']]['intervals']:
        date1 = datetime.strptime(t1, '%Y%m%d').date()
        date = datetime.strptime(row['day'], '%Y%m%d').date()
        date2 = datetime.strptime(t2, '%Y%m%d').date()
        if date1 - timedelta(days=1) <= date <= date2:
            return True
    return False


def remove_bad_accesses_from_parquet():
    print(f'Removing bad accesses from "data_accesses_sim.parquet"...', flush=True)
    df = pd.read_parquet('./../data/data_accesses_sim.parquet')
    with open('./../data/data_replicas_on_disk.json') as file:
        data = json.load(file)
    df = df[df['d_dataset'].isin(set(data.keys()))]
    df = df[df.progress_apply(lambda row: filter(row, data), axis=1)]
    df.reset_index(drop=True).to_parquet('./../data/data_accesses_sim.parquet')


def create_data_accesses_by_month_json():
    print(f'Creating "data_accesses_by_month.json"...', flush=True)
    with open('./../data/data_replicas_on_disk.json') as file:
        replicas = json.load(file)
    df = pd.read_parquet('./../data/data_accesses_sim.parquet')
    df['month'] = df['day'].apply(lambda day: f'{day[:4]}-{day[4:6]}')
    data = {dataset: {month: 0 for month in replicas[dataset]['months']}
            for dataset in df['d_dataset'].unique()}
    for _, row in tqdm(df.iterrows()):
        d, m, n = row['d_dataset'], row['month'], row['num_accesses']
        data[d][m] = data[d][m] + n if m in data[d] else n
    with open('./../data/data_accesses_by_month.json', mode='w') as file:
        json.dump(data, file, indent=2)


def get_datasets_info(df, datasets_names, name_to_index):
    print(f'Getting datasets info...', flush=True)
    datasets_info = {}
    for name in tqdm(datasets_names):
        row = df.loc[name_to_index[name]]
        datasets_info[name] = {'full_name': row['d_dataset'],
                               'tot_size': row['dsize'],
                               'num_files': row['nfiles'],
                               'num_events': row['devts'],
                               'data_tier': row['tier']}
    return datasets_info


def get_replicas_info(df, datasets_names):
    print(f'Getting replicas info...', flush=True)
    df = df[df['dataset_name'].isin(datasets_names)]
    replicas_info = {dataset: {'num_replicas': len(dframe),
                               'mean_size_replicas': dframe['rep_size'].mean(),
                               'num_sites_replicas': dframe['node_name'].nunique()}
                     for dataset, dframe in tqdm(df.groupby('dataset_name'))}
    return replicas_info


def get_accesses_info(datasets_names):
    print(f'Getting accesses info...', flush=True)
    with open('./../data/data_accesses_by_month.json', mode='r') as file:
        data = json.load(file)
    accesses_info = {dataset: {'mean_accesses/month': np.mean(list(data[dataset].values())),
                               'std_accesses/month': np.std(list(data[dataset].values())),
                               'median_accesses/month': np.median(list(data[dataset].values()))}
                     for dataset in tqdm(datasets_names)}
    return accesses_info


def create_pop_features_parquet():
    df1 = pd.read_parquet('./../data/datasets_list_sim.parquet')
    dset_to_idx = {dset: idx
                   for idx, dset in df1['d_dataset'].to_dict().items()}
    df2 = pd.read_parquet('./../data/data_replicas_sim.parquet')
    df3 = pd.read_parquet('./../data/data_accesses_sim.parquet')
    with open('./../data/datasets_mcm_info.json', mode='r') as file:
        mcm_raw = json.load(file)
    pags = set(utils.get_pags())
    mcm = {}
    for dataset_name in mcm_raw:
        dataset_info = mcm_raw[dataset_name]
        pwg = dataset_info['pwg']
        campaign = dataset_info['campaign']
        generator = dataset_info['generator']
        if pwg in pags and campaign != 'None' and generator != 'None':
            mcm[dataset_name] = {'pag': pwg,
                                 'campaign': campaign,
                                 'generator': generator}
    datasets_names = set.intersection(set(df1['d_dataset']), set(df2['dataset_name']),
                                      set(df3['d_dataset']), set(mcm.keys()))
    info1 = get_datasets_info(df1, datasets_names, dset_to_idx)
    info2 = get_replicas_info(df2, datasets_names)
    info3 = get_accesses_info(datasets_names)
    print('Creating "pop_features.parquet"...', flush=True, end='')
    keys1 = ['full_name', 'tot_size', 'num_files', 'num_events', 'data_tier']
    mcm_keys = ['pag', 'campaign', 'generator']
    keys2 = ['num_replicas', 'mean_size_replicas', 'num_sites_replicas']
    keys3 = ['mean_accesses/month', 'std_accesses/month',
             'median_accesses/month']
    pop_dict = {dset_to_idx[dset]: [info1[dset][k] for k in keys1] +
                [mcm[dset][k] for k in mcm_keys] +
                [info2[dset][k] for k in keys2] +
                [info3[dset][k] for k in keys3]
                for dset in datasets_names}
    cols = keys1 + mcm_keys + keys2 + keys3
    pop_df = pd.DataFrame.from_dict(
        pop_dict, orient='index', columns=cols).reset_index(drop=True)
    pop_df.to_parquet('./../data/pop_features.parquet')
    print(' Done')


if __name__ == '__main__':

    print('\nSTEP-1')
    create_datasets_list_sim_parquet()
    create_data_replicas_sim_parquet()
    create_data_accesses_sim_parquet()

    print('\nSTEP-2')
    create_datasets_mcm_info_json()

    print('\nSTEP-3')
    create_data_replicas_on_disk_json()
    remove_bad_accesses_from_parquet()
    create_data_accesses_by_month_json()

    print('\nSTEP-4')
    create_pop_features_parquet()
