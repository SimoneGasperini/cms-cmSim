import os
import pandas as pd


def generate_new_files(inputfile, datatiers, include_sim_data=True):
    df = _read_input_df(inputfile)
    for dtier in datatiers:
        selection = [dtier, dtier+'SIM'] if include_sim_data else [dtier]
        df_part = df[df['tier'].isin(selection)]
        outputfile = './../data/' + dtier.lower() + '_data_history.parquet'
        df_part.to_parquet(outputfile)
        _print_message(outputfile)


def _read_input_df(inputfile):
    print('Reading input file... ', end='', flush=True)
    df = pd.read_parquet(inputfile)
    print('Done')
    return df


def _print_message(outputfile):
    dirname = os.path.dirname(outputfile)
    fname = os.path.basename(outputfile)
    print(f'New file "{fname}" succesfully created in "{dirname}/"')


if __name__ == '__main__':

    inputfile = './../data/dataset_site_info.parquet'
    datatiers = ['RAW', 'RECO', 'AOD', 'MINIAOD', 'NANOAOD']

    generate_new_files(inputfile=inputfile,
                       datatiers=datatiers,
                       include_sim_data=True)
