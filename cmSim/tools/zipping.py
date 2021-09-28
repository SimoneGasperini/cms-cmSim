import zlib
import json
import base64

ZIPJSON_KEY = 'base64(zip(o))'


def zip_json(j):
    j = {ZIPJSON_KEY:
         base64.b64encode(
             zlib.compress(
                 json.dumps(j).encode('utf-8')
             )
         ).decode('ascii')
         }
    return j


def unzip_json(j):
    try:
        j = zlib.decompress(base64.b64decode(j[ZIPJSON_KEY]))
    except:
        raise RuntimeError('Could not decode/unzip the contents')
    try:
        j = json.loads(j)
    except:
        raise RuntimeError('Could not interpret the unzipped contents')
    return j


def load_zipped_json(filepath):
    with open(filepath, mode='r') as f:
        j = unzip_json(json.load(f))
    return j


def dump_zipped_json(j, filepath):
    with open(filepath, mode='w') as f:
        json.dump(zip_json(j), f)


if __name__ == '__main__':

    filepath = './../../data/zip_mcm_dump.json'
    data = load_zipped_json(filepath)

    name = '/SingleElectronPt35/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM'
    result = data[name]
    print(f'RESULT KEYS = {list(result.keys())}')

    pd_name = result['dataset_name']
    pwg = result['pwg']
    campaign = result['member_of_campaign']

    print(f'PRIMARY DATASET NAME = {pd_name}')
    print(f'PWG = {pwg}')
    print(f'CAMPAIGN = {campaign}')
