import re

from cmSim.config.countries import COUNTRIES_CODE_TO_NAME, COUNTRIES_NAME_TO_CODE
from cmSim.config.datalakes import DATALAKE_TO_COUNTRIES, COUNTRY_TO_DATALAKE
from cmSim.config.pwgs import PWGs, PWGs_TO_MERGE
from cmSim.config.physics import KEYWORD_TO_PARTICLE, KEYWORD_TO_PAG


def get_countryName_from_countryCode(code):
    if code in COUNTRIES_CODE_TO_NAME:
        return COUNTRIES_CODE_TO_NAME[code]
    else:
        raise KeyError(f'The country code "{code}" is not valid!')


def get_countryCode_from_countryName(name):
    if name in COUNTRIES_NAME_TO_CODE:
        return COUNTRIES_NAME_TO_CODE[name]
    else:
        raise KeyError(f'The country name "{name}" is not valid!')


def get_countries_in_datalake(datalake):
    if datalake in DATALAKE_TO_COUNTRIES:
        return DATALAKE_TO_COUNTRIES[datalake]
    else:
        raise KeyError(f'The datalake "{datalake}" is not valid!')


def get_datalake_from_country(country):
    if country in COUNTRY_TO_DATALAKE:
        return COUNTRY_TO_DATALAKE[country]
    else:
        raise KeyError(f'The country "{country}" is not valid!')


def get_country_by_site(site):
    code = site.split('_')[1]
    return get_countryName_from_countryCode(code)


def get_countries():
    return set(COUNTRIES_NAME_TO_CODE.keys())


def get_pags():
    pags = set(PWGs['PAGs'].keys())
    for pwg in PWGs_TO_MERGE:
        pags.discard(pwg)
    return pags


def get_pogs():
    pogs = set(PWGs['POGs'].keys())
    for pwg in PWGs_TO_MERGE:
        pogs.discard(pwg)
    return pogs


def get_dpgs():
    dpgs = set(PWGs['DPGs'].keys())
    for pwg in PWGs_TO_MERGE:
        dpgs.discard(pwg)
    return dpgs


def merge_pwgs_in_dataframe(df):
    for old_pwg in PWGs_TO_MERGE:
        new_pwg = PWGs_TO_MERGE[old_pwg]
        df.loc[df['pwg'] == old_pwg, 'pwg'] = new_pwg
    return df


def guess_pag_from_name(dataset_name):
    # reference: https://opendata.cern.ch/docs/cms-simulated-dataset-names
    pd_name = dataset_name.split('/')[1]
    pd_name = re.sub(r'[^0-9a-zA-Z]', ' ', pd_name)
    for key in KEYWORD_TO_PAG:
        if key in pd_name.lower():
            return KEYWORD_TO_PAG[key]
    particles = __get_particles(pd_name)
    return __particles_to_pag(particles)


def __get_particles(pd_name):
    process = re.sub(r'(?<=\w)([A-Z0-9])', r' \1', pd_name)
    process = re.sub(r'[0-9]', '', process)
    process = re.sub(r' To ', ' ', process)
    particles = set(KEYWORD_TO_PARTICLE[key] for key in process.split()
                    if key in KEYWORD_TO_PARTICLE)
    return particles


def __particles_to_pag(particles):
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
