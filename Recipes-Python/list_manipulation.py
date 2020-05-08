# Author:   Matt J Williams
#           http://www.mattjw.net
#           mattjw@mattjw.net
# Date:     2016


def split_balanced(seq, num):
    """
    Split a list into exactly `num` groups.
    This will ensure that the sizes of those groups are roughly
    similar. The difference between the smallest and largest group size
    will be miminised. The largest groups will appear first.
    """
    # (If numpy avail, can be done quick with rounding and np.linspace?)
    assert num >= 1
    
    def get_group_sizes(seq_len, num_groups):
        # return size of first group in a list of len
        # `seq_len` that's being split into `num_groups`
        if num_groups == 1:
            return [seq_len]
        else:
            group_size = int(round(seq_len / float(num_groups)))
            return [group_size] + get_group_sizes(seq_len - group_size, num_groups-1)
    group_sizes = get_group_sizes(len(seq), num)
    group_sizes = list(sorted(group_sizes, reverse=True))
    assert sum(group_sizes) == len(seq)
    
    i = 0
    for group_size in group_sizes:
        yield seq[i:i+group_size]
        i += group_size