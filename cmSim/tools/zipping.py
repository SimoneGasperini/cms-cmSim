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
