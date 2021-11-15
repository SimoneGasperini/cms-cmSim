import re
from cmSim.tools import zipping

from cmSim.config.countries import COUNTRY_CODE_TO_COUNTRY_NAME, COUNTRY_NAME_TO_COUNTRY_CODE
from cmSim.config.datalakes import DATALAKE_TO_COUNTRIES, COUNTRY_TO_DATALAKE
from cmSim.config.pwgs import PWGS, PWGS_TO_MERGE
from cmSim.config.physics import KEYWORD_TO_PARTICLE, KEYWORD_TO_PAG


def get_countries():
    countries = list(COUNTRY_NAME_TO_COUNTRY_CODE.keys())
    return countries


def get_tier_from_site(site):
    tier = site.split('_')[0]
    return tier


def get_country_from_site(site):
    code = site.split('_')[1]
    country = get_countryName_from_countryCode(code)
    return country


def get_countryName_from_countryCode(code):
    if code in COUNTRY_CODE_TO_COUNTRY_NAME:
        name = COUNTRY_CODE_TO_COUNTRY_NAME[code]
        return name
    raise KeyError(f'The country code "{code}" is not valid!')


def get_countryCode_from_countryName(name):
    if name in COUNTRY_NAME_TO_COUNTRY_CODE:
        code = COUNTRY_NAME_TO_COUNTRY_CODE[name]
        return code
    raise KeyError(f'The country name "{name}" is not valid!')


def get_datalakes():
    datalakes = list(DATALAKE_TO_COUNTRIES.keys())
    return datalakes


def get_countries_in_datalake(datalake):
    if datalake in DATALAKE_TO_COUNTRIES:
        countries = DATALAKE_TO_COUNTRIES[datalake]
        return countries
    raise KeyError(f'The datalake "{datalake}" is not valid!')


def get_datalake_from_country(country):
    if country in COUNTRY_TO_DATALAKE:
        datalake = COUNTRY_TO_DATALAKE[country]
        return datalake
    raise KeyError(f'The country "{country}" is not valid!')


def get_datalake_from_site(site):
    country = get_country_from_site(site)
    datalake = get_datalake_from_country(country)
    return datalake


def get_pwgs(group=None):
    all_groups = list(PWGS.keys())
    if group is not None and group not in all_groups:
        raise KeyError(f'The group of PWGs "{group}" is not valid!')
    groups = [group] if group is not None else all_groups
    pwgs = []
    for grp in groups:
        pwgs += list(PWGS[grp].keys())
    for pwg in PWGS_TO_MERGE:
        if pwg in pwgs:
            pwgs.remove(pwg)
    return pwgs


def get_pwgName_from_pwgCode(code):
    for grp in list(PWGS.keys()):
        pwg_name = PWGS[grp].get(code, None)
        if pwg_name is not None:
            return pwg_name
    raise KeyError(f'The PWG code "{code}" is not valid!')


def get_pwg_from_dataset(dataset, mcm_data):
    if dataset not in mcm_data:
        return 'None'
    pwg = mcm_data[dataset]['pwg']
    if pwg in PWGS_TO_MERGE:
        pwg = PWGS_TO_MERGE[pwg]
    return pwg


def get_pag_to_color():
    pag_to_color = {
        'SMP': 'tab:blue',
        'TOP': 'tab:orange',
        'BPH': 'tab:red',
        'HIG': 'tab:green',
        'SUS': 'tab:purple',
        'EXO': 'tab:cyan',
        'HIN': 'tab:olive',
        'B2G': 'tab:brown',
        'Other PWG': 'gray',
        'Not found': 'black'}
    return pag_to_color


def get_datatier_to_color():
    datatier_to_color = {
        'RAW': 'tab:blue',
        'RECO': 'tab:cyan',
        'AOD': 'tab:green',
        'MINIAOD': 'tab:purple',
        'NANOAOD': 'tab:brown',
        'AODSIM': 'tab:red',
        'MINIAODSIM': 'tab:orange',
        'NANOAODSIM': 'tab:olive',
        'Other': 'gray'}
    return datatier_to_color


def get_mcm_data(filepath):
    print('Unzipping and loading json file... ', end='')
    mcm_data = zipping.load_zipped_json(filepath)
    print('Done', flush=True)
    return mcm_data


def guess_pag_from_name(dataset_name):
    # reference: https://opendata.cern.ch/docs/cms-simulated-dataset-names
    pd_name = dataset_name.split('/')[1]
    pd_name = re.sub(r'[^0-9a-zA-Z]', ' ', pd_name)
    for key in KEYWORD_TO_PAG:
        if key in pd_name.lower():
            return KEYWORD_TO_PAG[key]
    particles = _get_particles_from_name(pd_name)
    pag = _get_pag_from_particles(particles)
    return pag


def _get_particles_from_name(pd_name):
    process = re.sub(r'(?<=\w)([A-Z0-9])', r' \1', pd_name)
    process = re.sub(r'[0-9]', '', process)
    process = re.sub(r' To ', ' ', process)
    particles = set(KEYWORD_TO_PARTICLE[key] for key in process.split()
                    if key in KEYWORD_TO_PARTICLE)
    return particles


def _get_pag_from_particles(particles):
    if 'higgs' in particles:
        return 'HIG'
    elif 'top' in particles:
        return 'TOP'
    elif 'bottom' in particles:
        return 'BPH'
    elif ('quark' in particles) or ('gluon' in particles) or ('meson' in particles) or ('baryon' in particles):
        return 'FSQ'
    elif len(particles) > 0:
        return 'SMP'
    else:
        return 'None'
