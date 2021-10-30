import os
import pandas as pd
import pylab as plt
from tqdm import tqdm
from cmSim.country import Country
from cmSim import utils


input_dir = './../data'
output_dir = './../plots/countries_storage_history'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

df = pd.read_parquet(f'{input_dir}/dataset_site_info.parquet')
mcm_data = utils.get_mcm_data(f'{input_dir}/zip_mcm_dump.json')

df['pwg'] = df['dataset_name'].apply(
    utils.get_pwg_from_dataset, mcm_data=mcm_data)

countries_names = utils.get_countries()
for name in tqdm(countries_names, desc='Plotting'):
    country = Country.from_dataframe(name=name, df=df)
    fig, ax = plt.subplots(figsize=(16, 10))
    country.plot_storage_history_by_site(ax=ax)
    fig.savefig(f'{output_dir}/data_{country.name}')
    plt.close()
    fig, ax = plt.subplots(figsize=(16, 10))
    country.plot_storage_history_by_pag(ax=ax, datatier='AODSIM')
    fig.savefig(f'{output_dir}/AODSIM_data_{country.name}')
    plt.close()
