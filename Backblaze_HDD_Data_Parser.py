import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import csv

# this is the file path for the files we want to analyze
pathName = r'R:\Python\BackBlaze Hard Drive Stats\data_Q3_2020'
dataDir = Path(pathName)
# glob will list out all files matching the argument passed (.csv in this case)
list_of_files = list(dataDir.glob('*.csv'))

# empty list because we need a list of dfs to iterate over for the concat function
df_list = []
for file in list_of_files[1:3]:
    df = pd.read_csv(file, sep=',', header=0, usecols=['smart_9_raw', 'model', 'capacity_bytes', 'failure'])
    df_list.append(df)
    print(f'File {file} done.')

# compile all the data into a single dataframe, using the prev. generated list as data
df = pd.concat(df_list, axis=0, ignore_index=True)

# change the units for capacity to gbytes instead of bytes
df['capacity_bytes'] = pd.to_numeric(df['capacity_bytes'], downcast='float')
df['capacity_bytes'] = df['capacity_bytes'] / 1_000_000_000

# rename the capacity column accordingly
df.rename(columns={'capacity_bytes' : 'capacity_gbytes'}, inplace=True)

# TODO add the rest of the data to our folder, and look at all data over all 7 years!
# typecast the failures column (0 or 1) as a float so we can do a comparison
df['failure'] = pd.to_numeric(df['failure'], downcast='float')
print(df['failure'].value_counts())
print(f'maximum power on hours = {df["smart_9_raw"].max()}')
print(f'average power on hours = {df["smart_9_raw"].mean()}')

# select only the failures (a failed drive has a '1' in this column)
failures = (df[df.failure >= 1])
print(f'maximum hours at failure = {failures["smart_9_raw"].max()}')
print(f'minimum hours at failure = {failures["smart_9_raw"].min()}')
print(f'average hours at failure = {failures["smart_9_raw"].mean()}')

print(df)
