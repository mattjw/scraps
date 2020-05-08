# Author:   Matt J Williams
#           http://www.mattjw.net
#           mattjw@mattjw.net
# Date:     2016

# IO for line-delimited JSON.


import json


def save_ldjson(seq, fpath):
    """
    Save sequence of objects `seq` as line delimited JSON to file at path
    `fpath` File ends with newline.
    """
    with open(fpath, 'w') as f:
        it = iter(seq)
        try:
            while True:
                obj = it.next()
                line = json.dump(obj, f)
                f.write('\n')
        except StopIteration:
            pass


def load_ldjson(fpath, extended_json=False):
    """
    Load sequence of JSON objects from file. Yields each object to allow
    iteration. Ignores blank lines.

    If `extended_json` is True, then read `fpath` as if it contains Extended
    JSON documents (as defined and output by MongoDB).
    """
    if extended_json:
        import bson.json_util

    with open(fpath, 'r') as f:
        for ln in f:
            if ln.strip() == '':
                continue
            if not extended_json:
                obj = json.loads(ln)
            else:
                obj = bson.json_util.loads(ln)
            yield obj


if __name__ == "__main__":
    for doc in load_ldjson('_example_data/example_ldjson.json'):
        print(doc['name'])
