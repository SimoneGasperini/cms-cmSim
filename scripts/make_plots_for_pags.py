import os
import pandas as pd
import pylab as plt
from tqdm import tqdm
from cmSim.container import DataContainer, get_datasets
from cmSim import utils

pd.options.mode.chained_assignment = None

input_dir = './../data'
output_dir = './../plots/pags_storage_history'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

df = pd.read_parquet(f'{input_dir}/dataset_site_info.parquet')
mcm_data = utils.get_mcm_data(f'{input_dir}/zip_mcm_dump.json')

df['pwg'] = df['dataset_name'].apply(
    utils.get_pwg_from_dataset, mcm_data=mcm_data)

pags = utils.get_pwgs(group='pags')
for pag in tqdm(pags, desc='Plotting'):
    datasets = get_datasets(df=df, pwg=pag, datatier='AODSIM')
    container = DataContainer.from_dataframe(datasets=datasets, df=df)
    fig, ax = plt.subplots(figsize=(16, 10))
    container.plot_storage_history_in_countries(ax=ax)
    fig.savefig(f'{output_dir}/{pag}_data_in_countries')
    plt.close()
    fig, ax = plt.subplots(figsize=(16, 10))
    container.plot_storage_history_in_datalakes(ax=ax)
    fig.savefig(f'{output_dir}/{pag}_data_in_datalakes')
    plt.close()
