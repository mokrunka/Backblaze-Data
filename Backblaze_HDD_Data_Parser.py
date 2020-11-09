import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import csv

# this is the file path for the files we want to analyze
# users should update this path to match the directory in which they've stored
# their own data
pathName = r'R:\Python\BackBlaze Hard Drive Stats\data_Q3_2020'
dataDir = Path(pathName)
# glob will list out all files matching the argument passed (.csv in this case)
list_of_files = list(dataDir.glob('*.csv'))

# empty list because we need a list of dfs to iterate over for the concat function
df_list = []
for file in list_of_files[:5]:
    df = pd.read_csv(file, sep=',', header=0, usecols=['smart_9_raw', 'model', 'capacity_bytes', 'failure'])
    df_list.append(df)
    print(f'File {file} done.')

# TODO remove all drives with less than 60 total drives

# compile all the data into a single dataframe, using the prev. generated list as data
df = pd.concat(df_list, axis=0, ignore_index=True)

# change the units for capacity to gbytes instead of bytes
df['capacity_bytes'] = pd.to_numeric(df['capacity_bytes'], downcast='float')
df['capacity_bytes'] = df['capacity_bytes'] / 1_000_000_000
# rename the capacity column accordingly
df.rename(columns={'capacity_bytes': 'capacity_gbytes'}, inplace=True)

# typecast the failures column (0 or 1) as a float so we can do a comparison
df['failure'] = pd.to_numeric(df['failure'], downcast='float')

# take all hours counts greater than 90k and make them their own data frame, then drop them
indexNames = df[(df['smart_9_raw'] >= 90_000)].index
df.drop(indexNames, inplace=True)

# count up the number of failures
# model_counts = df['model'].value_counts()
# print(model_counts)
num_failures = df['failure'].value_counts()
failed_drives = num_failures.loc[1]
# compute the daily failure rate = number of drive failures / total drive days (rows)
DFR = round((failed_drives / len(df)) * 100, 4)
print('Drive Days: ', len(df))

# compute the maximum power on hours of all drives
print(f'Maximum power on hours = {df["smart_9_raw"].max():,}')

# compute the average power on hours of all drives
print(f'Average power on hours = {df["smart_9_raw"].mean():,}')

# select only the failures (a failed drive has a '1' in this column)
failures = (df[df.failure >= 1])
print(f'Maximum hours at failure = {failures["smart_9_raw"].max():,}')
print(f'Minimum hours at failure = {failures["smart_9_raw"].min():,}')
print(f'Average hours at failure = {failures["smart_9_raw"].mean():,}')
print(f'Total number of drive failures: {failed_drives}')
print(f'Daily failure rate (DFR, %) =  {DFR}')

print(f'Annual failure rate (AFR, %) =  {DFR * 365}')
