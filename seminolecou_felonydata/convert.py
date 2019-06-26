import pandas as pd
from ast import literal_eval


def clean():

    with open('felo_data.jsonl') as f:
        records = [literal_eval(line) for line in f]

    felodf = pd.DataFrame.from_records(records).set_index('id')

    cols = [i for i in felodf.columns]
    cols = cols[4:] + cols[:3]
    num_unique = max([len(felodf[i].unique()) for i in cols])

    felodf = felodf.drop_duplicates(['ucn', 'name'])

    if num_unique == len(felodf):
        print("duplicates removed.")
