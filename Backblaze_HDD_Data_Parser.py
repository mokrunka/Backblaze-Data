import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import csv

# this is the file path for the files we want to analyze
# users should update this path to match the directory in which they've stored
# their own data
pathName = r'R:\Python\BackBlaze Hard Drive Stats\All Raw Data'
dataDir = Path(pathName)
# glob will list out all files matching the argument passed (.csv in this case)
list_of_files = list(dataDir.glob('*.csv'))

# empty list because we need a list of dfs to iterate over for the concat function
df_list = []
for file in list_of_files[1:6]:
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

# typecast the failures column (0 or 1) as a float so we can do a comparison
df['failure'] = pd.to_numeric(df['failure'], downcast='float')

# count up the number of failures
num_failures = df['failure'].value_counts()
# compute the daily failure rate = number of drive failures / total drive days (rows)
DFR = num_failures / len(df.index)
print('drive days', len(df.index))
print('dfr ', DFR)

# TODO BB mentions some of the power on hours are out of bounds, and '10+ years' is not
# TODO possible. we should at least drop all data with drives > 10 yrs old
# compute the maximum power on hours of all drives
print(f'maximum power on hours = {df["smart_9_raw"].max()}')

# compute the average power on hours of all drives
print(f'average power on hours = {df["smart_9_raw"].mean()}')

# select only the failures (a failed drive has a '1' in this column)
failures = (df[df.failure >= 1])
print(f'maximum hours at failure = {failures["smart_9_raw"].max()}')
print(f'minimum hours at failure = {failures["smart_9_raw"].min()}')
print(f'average hours at failure = {failures["smart_9_raw"].mean()}')
print(f'Total number of drive failures: {num_failures}')
print(f'daily failure rate (DFR, %) =  {DFR * 100}')
print(f'annual failure rate (AFR, %) =  {DFR * 100 * 365}')

# print(df)
