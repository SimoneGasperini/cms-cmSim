import re


# dictionary mapping each physics keyword to the corresponding official PAG
keyword_to_pag = {
    'exo': 'EXOTICA',
    'black': 'EXOTICA',
    'dark': 'EXOTICA',
    'grav': 'EXOTICA',
    'qstar': 'EXOTICA',
    'bstar': 'EXOTICA',
    'tstar': 'EXOTICA',
    'seesawtype': 'EXOTICA',
    'radion': 'EXOTICA',
    'branon': 'EXOTICA',
    'axion': 'EXOTICA',
    'forward': 'Forward and QCD',
    'qcd': 'Forward and QCD',
    'gluon': 'Forward and QCD',
    'jets': 'Forward and QCD',
    'hig': 'Higgs',
    'vbf': 'Higgs',
    'htautau': 'Higgs',
    'haa': 'Higgs',
    'hbb': 'Higgs',
    'hgg': 'Higgs',
    'susy': 'SUSY',
    'rpc': 'SUSY',
    'rpv': 'SUSY',
    't2tt': 'SUSY',
    't2cc': 'SUSY',
    't1tttt': 'SUSY',
    't1bbbb': 'SUSY',
    't1qqqq': 'SUSY',
    't2qq': 'SUSY',
    't6ttww': 'SUSY',
    'ewk': 'SUSY',
    'pmssm': 'Standard Model',
    'muplusandminus': 'Standard Model',
    'wjet': 'Standard Model',
    'zjet': 'Standard Model',
    'dy': 'Standard Model',
    'tzq': 'Standard Model',
    'monophoton': 'Standard Model',
    'monojet': 'Standard Model',
    'atautau': 'Standard Model',
    'zgamma': 'Standard Model',
    'zgg': 'Standard Model',
    'ze': 'Standard Model',
    'zmu': 'Standard Model',
    'ztau': 'Standard Model',
    'znu': 'Standard Model',
    'zprime': 'Standard Model',
    'zbb': 'Standard Model',
    'wgamma': 'Standard Model',
    'wgg': 'Standard Model',
    'we': 'Standard Model',
    'wenu': 'Standard Model',
    'wmu': 'Standard Model',
    'wtau': 'Standard Model',
    'wnu': 'Standard Model',
    'wprime': 'Standard Model',
    'minbias': 'Standard Model',
    'bottom': 'B-Physics',
    'bjet': 'B-Physics',
    'bbar': 'B-Physics',
    'phibb': 'B-Physics',
    'benriched': 'B-Physics',
    'top': 'Top-Physics',
    'tjet': 'B-Physics',
    'tbar': 'Top-Physics',
    'b2g': 'Beyond-two-Generations',
    'vlq': 'Beyond-two-Generations',
    'vhf': 'Beyond-two-Generations',
    'vector': 'Beyond-two-Generations',
    'diboson': 'Beyond-two-Generations',
    'dijet': 'Beyond-two-Generations',
    'trijet': 'Beyond-two-Generations'
}


# dictionary mapping each particle keyword to the corresponding particle name
particles_dict = {
    'Electron': 'electron',
    'Electrons': 'electron',
    'Positron': 'electron',
    'Positrons': 'electron',
    'E': 'electron',
    'Eplus': 'electron',
    'Ep': 'electron',
    'Eminus': 'electron',
    'Em': 'electron',
    'Muon': 'muon',
    'Muons': 'muon',
    'Mu': 'muon',
    'Muplus': 'muon',
    'Muminus': 'muon',
    'Tau': 'tau',
    'Tauplus': 'tau',
    'Tauminus': 'tau',
    'Lepton': 'charged lepton',
    'Leptons': 'charged lepton',
    'lept': 'charged lepton',
    'Lept': 'charged lepton',
    'L': 'charged lepton',
    'Neutrino': 'neutrino',
    'Nu': 'neutrino',
    'Nue': 'neutrino',
    'Numu': 'neutrino',
    'Nutau': 'neutrino',
    'Nuebar': 'neutrino',
    'Numubar': 'neutrino',
    'Nutaubar': 'neutrino',
    'W': 'W',
    'Wplus': 'W',
    'Wp': 'W',
    'Wminus': 'W',
    'Wm': 'W',
    'Wprime': 'W',
    'Z': 'Z',
    'Zprime': 'Z',
    'Zp': 'Z',
    'Photon': 'photon',
    'G': 'photon',
    'Gamma': 'photon',
    'Gluon': 'gluon',
    'Glu': 'gluon',
    'Top': 'top',
    'T': 'top',
    'Tbar': 'top',
    'Tprime': 'top',
    'Tp': 'top',
    'Bottom': 'bottom',
    'B': 'bottom',
    'Bbar': 'bottom',
    'Bprime': 'bottom',
    'Bp': 'bottom',
    'Upsilon': 'bottom',
    'Quark': 'quark',
    'Quarks': 'quark',
    'Q': 'quark',
    'Qbar': 'quark',
    'H': 'higgs',
    'Hplus': 'higgs',
    'Hp': 'higgs',
    'Hminus': 'higgs',
    'Hm': 'higgs',
    'Rho': 'meson',
    'Phi': 'meson',
    'Eta': 'meson',
    'Etazero': 'meson',
    'Psi': 'meson',
    'Jpsi': 'meson',
    'Pion': 'meson',
    'Pi': 'meson',
    'Kaon': 'meson',
    'K': 'meson',
    'Kplus': 'meson',
    'Kminus': 'meson',
    'Kstar': 'meson',
    'D': 'meson',
    'Lambda': 'baryon',
    'Delta': 'baryon',
    'Sigma': 'baryon',
    'Xi': 'baryon',
    'Omega': 'baryon'
}


def get_pag(dataset_name):
    pd_name = dataset_name.split('/')[1]
    pd_name = re.sub(r'[^0-9a-zA-Z]', ' ', pd_name)
    for key in keyword_to_pag:
        if key in pd_name.lower():
            return keyword_to_pag[key]
    particles = _get_particles(pd_name)
    pag = _particles_to_pag(particles)
    if pag is None:
        print(dataset_name)
    return pag


def _get_particles(process):
    # insert a space before capital letters or numbers
    process = re.sub(r'(?<=\w)([A-Z0-9])', r' \1', process)
    process = re.sub(r'[0-9]', '', process)
    process = re.sub(r' To ', ' ', process)
    return set(particles_dict[key] for key in process.split() if key in particles_dict)


def _particles_to_pag(particles):
    if 'higgs' in particles:
        return 'Higgs'
    elif 'top' in particles:
        return 'Top-Physics'
    elif 'bottom' in particles:
        return 'B-Physics'
    elif ('quark' in particles) or ('gluon' in particles) or ('meson' in particles) or ('baryon' in particles):
        return 'Forward and QCD'
    elif len(particles) > 0:
        return 'Standard Model'
    else:
        return 'UNKNOWN'


if __name__ == '__main__':

    import pandas as pd

    filepath = './data/dataset_site_info.parquet'
    #filepath = './data/dataset_size_info.parquet'

    df = pd.read_parquet(filepath)
    df = df[df['tier'] == 'AODSIM']

    datasets_df = df[['dataset_name']].drop_duplicates()
    #datasets_df = df[['d_dataset']]

    datasets_df['PAG'] = datasets_df['dataset_name'].apply(get_pag)
    #datasets_df['PAG'] = datasets_df['d_dataset'].apply(get_pag)

    unknown_pag_df = datasets_df[datasets_df['PAG'] == 'UNKNOWN']
    print(f'total number of AODSIM datasets = {len(datasets_df)}')
    print(f'number of unknown PAG datasets = {len(unknown_pag_df)}')
    pags = set(datasets_df['PAG'])
    print(f'PAGs = {pags}')

    with pd.option_context('display.max_colwidth', None):
        print(datasets_df[datasets_df['PAG'] == 'UNKNOWN'][:10])
