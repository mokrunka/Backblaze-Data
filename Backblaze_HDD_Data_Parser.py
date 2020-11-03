import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import csv

# this is the file path for the files we want to analyze
pathName = r'R:\Python\BackBlaze Hard Drive Stats\data_Q3_2020'
dataDir = Path(pathName)
list_of_files = list(dataDir.glob('*.csv'))

# empty list because we need a list of dfs to iterate over for the concat function
df_list = []
for file in list_of_files[1:5]:
    df = pd.read_csv(file, sep=',', header=0, usecols=['smart_9_raw', 'model', 'capacity_bytes', 'failure'])
    df_list.append(df)
    print(f'File {file} done.')

df = pd.concat(df_list, axis=0, ignore_index=True)
print(df)


print(df['failure'].value_counts())
