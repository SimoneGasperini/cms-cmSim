from itertools import chain


# dictionary mapping each particle (or particles class) to the corresponding set of keywords
# --> all the keywords must start with a capital letter
PARTICLE_TO_KEYWORDS = \
    {
        'W':
        {
            'W',
            'Wplus',
            'Wp',
            'Wminus',
            'Wm',
            'Wprime'
        },
        'Z':
        {
            'Z',
            'Zprime',
            'Zp'
        },
        'baryon':
        {
            'Lambda',
            'Omega',
            'Delta',
            'Xi',
            'Sigma'
        },
        'bottom':
        {
            'B',
            'Bottom',
            'Bprime',
            'Bp',
            'Bbar',
            'Upsilon'
        },
        'charged lepton':
        {
            'L',
            'Lepton',
            'Leptons',
            'Lept'
        },
        'electron':
        {
            'E',
            'Electron',
            'Electrons',
            'Eplus',
            'E',
            'Eminus',
            'Em',
            'Positron',
            'Positrons'},
        'gluon':
        {
            'Gluon',
            'Glu'
        },
        'higgs':
        {
            'H',
            'Hplus',
            'Hp',
            'Hminus',
            'Hm'
        },
        'meson':
        {
            'D',
            'Eta',
            'Etazero',
            'Jpsi',
            'K',
            'Kaon',
            'Kplus',
            'Kminus',
            'Kstar',
            'Phi',
            'Pi',
            'Pion',
            'Psi',
            'Rho'
        },
        'muon':
        {
            'Mu',
            'Muon',
            'Muons',
            'Muplus',
            'Muminus'
        },
        'neutrino':
        {
            'Nu',
            'Neutrino',
            'Nue',
            'Nuebar',
            'Numu',
            'Numubar',
            'Nutau',
            'Nutaubar'
        },
        'photon':
        {
            'G',
            'Gamma',
            'Photon'
        },
        'quark':
        {
            'Q',
            'Quark',
            'Quarks',
            'Qbar'
        },
        'tau':
        {
            'Tau',
            'Tauplus',
            'Tauminus'
        },
        'top':
        {
            'T',
            'Top',
            'Tprime',
            'Tp',
            'Tbar'
        }
    }


keywords1 = set(chain(*(PARTICLE_TO_KEYWORDS[particle]
                        for particle in PARTICLE_TO_KEYWORDS)))


KEYWORD_TO_PARTICLE = {keyword: particle for keyword in keywords1
                       for particle in PARTICLE_TO_KEYWORDS
                       if keyword in PARTICLE_TO_KEYWORDS[particle]}


# dictionary mapping each PAG (3-letters code) to the corresponding set of keywords
# --> all the keywords letters must be in lower case
PAG_TO_KEYWORDS = \
    {
        'SMP':
        {
            'atautau',
            'dy',
            'minbias',
            'monojet',
            'monophoton',
            'muplusandminus',
            'pmssm',
            'tzq',
            'we',
            'wenu',
            'wgamma',
            'wgg',
            'wjet',
            'wmu',
            'wnu',
            'wprime',
            'wtau',
            'zbb',
            'ze',
            'zgamma',
            'zgg',
            'zjet',
            'zmu',
            'znu',
            'zprime',
            'ztau'
        },
        'TOP':
        {
            'top',
            'tbar',
            'tjet'
        },
        'BPH':
        {
            'bottom',
            'bjet',
            'benriched',
            'bbar',
            'phibb'
        },
        'FSQ':
        {
            'fwd',
            'forward',
            'gluon',
            'gluino',
            'qcd',
            'jets'
        },
        'HIG':
        {
            'hig',
            'hgg',
            'haa',
            'hbb',
            'htautau',
            'vbf'
        },
        'SUS':
        {
            'susy',
            'ewk',
            'rpc',
            'rpv',
            't1bbbb',
            't1qqqq',
            't1tttt',
            't2cc',
            't2qq',
            't2tt',
            't6ttww'
        },
        'EXO':
        {
            'exo',
            'dark',
            'black',
            'radion',
            'axion',
            'branon',
            'grav',
            'qstar',
            'bstar',
            'tstar',
            'seesawtype'
        },
        'HIN':
        {
            'heavy',
            'ions'
        },
        'B2G':
        {
            'b2g',
            'diboson',
            'dijet',
            'trijet',
            'vector',
            'vhf',
            'vlq'
        }
    }


keywords2 = set(chain(*(PAG_TO_KEYWORDS[pag] for pag in PAG_TO_KEYWORDS)))


KEYWORD_TO_PAG = {keyword: pag for keyword in keywords2
                  for pag in PAG_TO_KEYWORDS
                  if keyword in PAG_TO_KEYWORDS[pag]}
