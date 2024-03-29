import os
import re
import json
import math
import itertools
import numpy as np
from datetime import datetime
from scipy import stats
from cmSim.tools import zipping


def load_json_file(filename):
    filepath = os.path.dirname(__file__) + '/config/' + filename
    with open(filepath, 'r') as file:
        dictionary = json.load(file)
    return dictionary


def remove_outliers_Zscore(arr, n=3):
    return arr[np.abs(stats.zscore(arr)) < n]


def remove_outliers_IQRscore(arr, n=3):
    q1 = np.quantile(arr, q=0.25)
    q3 = np.quantile(arr, q=0.75)
    iqr = q3 - q1
    return arr[(q1 - n*iqr < arr) & (arr < q3 + n*iqr)]


def get_string_from_date(date, format='%y%m%d'):
    return date.strftime(format)


def get_date_from_string(string, format='%y%m%d'):
    return datetime.strptime(string, format).date()


def get_day_to_week(days):
    day_to_week = {day: f'{year}-week{str(i//7 + 1).zfill(2)}'
                   for year, ds in itertools.groupby(days, lambda day: f'20{day[:2]}')
                   for i, day in enumerate(ds)}
    return day_to_week


def get_day_to_month(days):
    day_to_month = {day: f'20{day[:2]}-{day[2:4]}'
                    for day in days}
    return day_to_month


def get_countries():
    countries_dict = load_json_file('countries.json')
    return sorted(list(countries_dict.keys()))


def get_tier_from_site(site):
    return site.split('_')[0]


def get_country_from_site(site):
    code = site.split('_')[1]
    return get_countryName_from_countryCode(code)


def get_countryName_from_countryCode(code):
    countries_dict = load_json_file('countries.json')
    for country in countries_dict:
        if code == countries_dict[country]['code']:
            return countries_dict[country]['name']
    raise KeyError(f'Country code "{code}" not found')


def get_countryCode_from_countryName(name):
    countries_dict = load_json_file('countries.json')
    if name in countries_dict:
        return countries_dict[name]['code']
    else:
        raise KeyError((f'Country "{name}" not found'))


def get_datalakes():
    datalakes_dict = load_json_file('datalakes.json')
    return sorted(list(datalakes_dict.keys()))


def get_countries_in_datalake(datalake):
    datalakes_dict = load_json_file('datalakes.json')
    if datalake in datalakes_dict:
        return datalakes_dict[datalake]['countries']
    raise KeyError(f'Datalake "{datalake}" not found')


def get_datalake_from_country(country):
    datalakes_dict = load_json_file('datalakes.json')
    for datalake in datalakes_dict:
        if country in datalakes_dict[datalake]['countries']:
            return datalake
    raise KeyError(f'Country "{country}" not found')


def get_datalake_from_site(site):
    country = get_country_from_site(site)
    return get_datalake_from_country(country)


def group_sites_by_datalake(sites):
    datalake_to_sites = {datalake: [] for datalake in get_datalakes()}
    for site in sites:
        datalake = get_datalake_from_site(site)
        datalake_to_sites[datalake].append(site)
    return datalake_to_sites


def get_datalake_to_color():
    datalakes_dict = load_json_file('datalakes.json')
    return {dl: datalakes_dict[dl]['color'] for dl in datalakes_dict}


def get_pwgs_to_merge():
    pwgs_to_merge = {}
    pwgs_dict = load_json_file('physics_groups.json')
    for group in pwgs_dict:
        for pwg in pwgs_dict[group]:
            if "merged_with" in pwgs_dict[group][pwg]:
                pwgs_to_merge[pwg] = pwgs_dict[group][pwg]['merged_with']
    return pwgs_to_merge


PWGS_TO_MERGE = get_pwgs_to_merge()


def get_pags():
    pwgs_dict = load_json_file('physics_groups.json')
    pags = sorted(list(pwgs_dict['PAGs'].keys()))
    for pag in pags:
        if pag in PWGS_TO_MERGE:
            pags.remove(pag)
    return pags


def get_pogs():
    pwgs_dict = load_json_file('physics_groups.json')
    pogs = sorted(list(pwgs_dict['POGs'].keys()))
    for pog in pogs:
        if pog in PWGS_TO_MERGE:
            pogs.remove(pog)
    return pogs


def get_dpgs():
    pwgs_dict = load_json_file('physics_groups.json')
    dpgs = sorted(list(pwgs_dict['DPGs'].keys()))
    for dpg in dpgs:
        if dpg in PWGS_TO_MERGE:
            dpgs.remove(dpg)
    return dpgs


def get_pwgName_from_pwgCode(code):
    pwgs_dict = load_json_file('physics_groups.json')
    for group in pwgs_dict:
        for pwg in pwgs_dict[group]:
            if code == pwgs_dict[group][pwg]['code']:
                return pwgs_dict[group][pwg]['name']
    raise KeyError(f'PWG code "{code}" not found')


def get_pwg_from_dataset(dataset, mcm_data):
    if dataset in mcm_data:
        pwg = mcm_data[dataset]['pwg']
        if pwg in PWGS_TO_MERGE:
            pwg = PWGS_TO_MERGE[pwg]
        return pwg
    else:
        return 'None'


def get_campaign_from_dataset(dataset, mcm_data):
    if dataset in mcm_data:
        campaign = mcm_data[dataset]['member_of_campaign']
        substrs = ['Winter\d{2}', 'Spring\d{2}',
                   'Summer\d{2}', 'Fall\d{2}', 'Autumn\d{2}']
        for substr in substrs:
            match = re.search(substr, campaign)
            if match is not None:
                season = match.group(0)
                break
        else:
            return 'None'
        if campaign.startswith('HIN'):
            return 'HIN-' + season
        if campaign.startswith('RunII'):
            return 'RunII-' + season
    return 'None'


def get_generator_from_dataset(dataset, mcm_data):
    valid_gens = ['evtgen', 'herwig', 'alpgen', 'mcatnlo', 'pythia6',
                  'sherpa', 'tauola', 'powheg', 'madgraph', 'pythia8']
    if dataset in mcm_data:
        gens_str = ''.join(mcm_data[dataset]['generators']) + dataset
        for gen in valid_gens:
            if gen in gens_str.lower():
                return gen
    return 'None'


def get_rounded_num_accesses(fract_read, max_num_accesses=None):
    num_accesses = math.ceil(fract_read)
    if max_num_accesses is None:
        return num_accesses
    else:
        return num_accesses if num_accesses <= max_num_accesses else max_num_accesses


def get_pag_to_color():
    pwgs_dict = load_json_file('physics_groups.json')
    pags = get_pags()
    pag_to_color = {pag: pwgs_dict['PAGs'][pag]['color'] for pag in pags}
    pag_to_color['Other PWG'] = 'gray'
    pag_to_color['Not found'] = 'black'
    return pag_to_color


def get_datatiers(type=None):
    datatiers_dict = load_json_file('data_tiers.json')
    if type is None:
        datatiers = sorted(list(datatiers_dict.keys()))
    else:
        datatiers = sorted([dt for dt in datatiers_dict
                            if datatiers_dict[dt]['type'] == type])
    return datatiers


def get_datatier_to_color():
    datatiers_dict = load_json_file('data_tiers.json')
    datatiers = sorted(list(datatiers_dict.keys()))
    datatier_to_color = {dt: datatiers_dict[dt]['color'] for dt in datatiers
                         if 'color' in datatiers_dict[dt]}
    datatier_to_color['Other'] = 'gray'
    return datatier_to_color


def get_mcm_data(filepath):
    print('Unzipping and loading json file... ', end='')
    mcm_data = zipping.load_zipped_json(filepath)
    print('Done', flush=True)
    return mcm_data
