def discard_duplicates(seq, key_func):
    """
    Discard any duplicates in`seq`. `key_func` is a function that assigns
    an item in `seq` to a key. Order is retained.
    """
    d = OrderedDict()
    for item in seq:
        key = key_func(item)
        if key not in d:
            d[key] = item
    return d.values()