import os
import pandas as pd
import pylab as plt
from tqdm import tqdm
from cmSim.site import Site
from cmSim import utils


input_dir = './../data'
output_dir = './../plots/sites_storage_history'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

df = pd.read_parquet(f'{input_dir}/dataset_site_info.parquet')
mcm_data = utils.get_mcm_data(f'{input_dir}/zip_mcm_dump.json')

df['pwg'] = df['dataset_name'].apply(
    utils.get_pwg_from_dataset, mcm_data=mcm_data)

nodes_names = df['node_name'].unique()
for name in tqdm(nodes_names, desc='Plotting'):
    site = Site.from_dataframe(name=name, df=df)
    fig, ax = plt.subplots(figsize=(16, 10))
    site.plot_storage_history_by_pag(ax=ax)
    fig.savefig(f'{output_dir}/data_{site.name}')
    plt.close()
