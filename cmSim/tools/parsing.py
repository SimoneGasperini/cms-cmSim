import json


def parse_mcm_txt(filepath, datatier='AODSIM'):
    """
    Parse the .txt file dumped from the McM API. The file must contain a request's result
    per line and each line must be structured as a json parsable nested dictionary.
    Only info about datasets of the specified datatier are returned.

    Parameters
    ----------
    filepath : str
        Path of the text file to be parsed
    datatier : str, optional
        Datatier of the datasets to be considered, by default 'AODSIM'

    Returns
    -------
    dict
        Dictionary mapping each dataset name to the corresponding info returned by McM
    """
    with open(filepath) as file:
        lines = file.readlines()
    data = {}
    for line in lines:
        parsed_dict = json.loads(line)
        datasets_list = [dataset for dataset in parsed_dict['output_dataset']
                         if dataset.endswith(datatier)]
        if not datasets_list:
            continue
        else:
            dataset_name = datasets_list[0]
            data[dataset_name] = parsed_dict
    return data


if __name__ == '__main__':

    filepath = './../../data/mcm_dump.txt'
    data = parse_mcm_txt(filepath)

    name = '/SingleElectronPt35/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM'
    result = data[name]
    print(f'RESULT KEYS = {list(result.keys())}')

    pd_name = result['dataset_name']
    pwg = result['pwg']
    campaign = result['member_of_campaign']

    print(f'PRIMARY DATASET NAME = {pd_name}')
    print(f'PWG = {pwg}')
    print(f'CAMPAIGN = {campaign}')
