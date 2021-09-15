# reference: https://twiki.cern.ch/twiki/bin/view/CMSPublic/PhysicsResultsConveners#Physics_and_Detector_Performance

PWGs = \
    {
        'PAGs':  # Physics Analysis Groups
        {
            'SMP': 'Standard Model',
            'TOP': 'Top Physics',
            'BPH': 'B Physics',
            'FSQ': 'Forward & Small-x QCD',  # merged with SMP
            'HIG': 'Higgs',
            'SUS': 'Susy',
            'EXO': 'Exotica',
            'HIN': 'Heavy Ions',
            'B2G': 'Beyond Two Generations'
        },

        'POGs':  # Physics Object Groups
        {
            'TRK': 'Tracking',
            'BTV': 'Btag and vertexing',
            'EGM': 'e-gamma',
            'JME': 'JetMet',
            'LUM': 'Lumi',
            'MUO': 'Muon',
            'TAU': 'Tau',
            'PRO': 'Protons',
            'GEN': 'Generators',
            'UPG': 'Upgrade Studies'
        },

        'DPGs':  # Detector Performance Groups
        {
            'TRACKER': 'Tracker',
            'ECAL': 'ECAL',
            'HCA': 'HCAL',
            'MUON': 'Muon',
            'DT': 'Muon DT',
            'CSC': 'Muon CSC',
            'RPC': 'Muon RPC',
            'GEM': 'Muon Gem',
            'L1T': 'Trigger L1',
            'BRIL': 'BRIL',
            'CTPPS': 'CT-PPS',
            'HGC': 'HGCAL',
            'MDT': 'MTD'
        },

        'others':
        {
            'EWK': 'Electroweak Physics',
            'FWD': 'Forward Physics',  # merged with SMP
            'PPD': 'Physics Performance & Dataset',
            'PPS': 'Precision Proton Spectrometer',
            'QCD': 'Quantum Chromo-Dynamics',  # merged with SMP
            'TSG': 'Trigger Studies',
            'CPF': '?',
            'None': '?'
        }
    }


PWGs_TO_MERGE = \
    {
        'FSQ': 'SMP',
        'FWD': 'SMP',
        'QCD': 'SMP'
    }
