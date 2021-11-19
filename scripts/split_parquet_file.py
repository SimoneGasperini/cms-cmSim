import os
import pandas as pd
from cmSim import utils


def generate_new_files(input_parquet, input_mcm_json):
    df = _load_input_df(input_parquet)
    for dtier in ['RAW', 'RECO']:
        df_part = df[df['tier'] == dtier]
        _write_output_df(df_part, dtier)
    mcm_data = _load_input_mcm(input_mcm_json)
    for dtier in ['AOD', 'MINIAOD', 'NANOAOD']:
        dtiers = [dtier, dtier+'SIM']
        df_part = df[df['tier'].isin(dtiers)]
        df_part['pwg'] = df_part['dataset_name'].apply(
            utils.get_pwg_from_dataset, mcm_data=mcm_data)
        df_part['campaign'] = df_part['dataset_name'].apply(
            utils.get_campaign_from_dataset, mcm_data=mcm_data)
        _write_output_df(df_part, dtier)


def _load_input_df(input_parquet):
    print('Reading input parquet file... ', end='', flush=True)
    df = pd.read_parquet(input_parquet)
    print('Done')
    return df


def _load_input_mcm(input_mcm_json, keys=['pwg', 'member_of_campaign']):
    data = {}
    for file in input_mcm_json:
        mcm = utils.get_mcm_data(file)
        d = {dataset: {key: mcm[dataset][key] for key in keys}
             for dataset in mcm}
        data = {**data, **d}
    return data


def _write_output_df(df, dtier):
    outputfile = './../data/' + dtier.lower() + '_data_history.parquet'
    df.to_parquet(outputfile)
    _print_message(outputfile)


def _print_message(outputfile):
    dirname = os.path.dirname(outputfile)
    fname = os.path.basename(outputfile)
    print(f'New file "{fname}" successfully created in "{dirname}/"')


if __name__ == '__main__':

    generate_new_files(input_parquet='./../data/dataset_site_info.parquet',
                       input_mcm_json=['./../data/aodsim_mcm_data.json',
                                       './../data/miniaodsim_mcm_data.json',
                                       './../data/nanoaodsim_mcm_data.json'])
