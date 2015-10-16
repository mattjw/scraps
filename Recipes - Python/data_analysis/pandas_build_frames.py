
#
#
# Construct from series of ordered dicts
#
rows = []
for dat in data:
    row = collections.OrderedDict()
    row['col1'] = 42
    rows.append(row)
df_cities = pandas.DataFrame(rows, columns=rows[0].keys())
