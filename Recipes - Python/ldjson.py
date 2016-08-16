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


def yield_ldjson(fpath):
    """
    Load sequence of JSON objects from file. Yields each object to allow
    iteration. Ignores blank lines.
    """
    with open(fpath, 'r') as f:
        for ln in f:
            if ln.strip() == '':
                continue
            obj = json.loads(ln)
            yield obj


if __name__ == "__main__":
    for doc in load_ldjson('_example_data/example_ldjson.json'):
        print doc['name']
