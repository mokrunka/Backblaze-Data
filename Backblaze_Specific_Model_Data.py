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
for file in list_of_files[-100:]:
    df = pd.read_csv(file, sep=',', header=0, usecols=['smart_9_raw', 'model', 'capacity_bytes', 'failure',
                                                       'serial_number'])
    df_list.append(df)
    print(f'File {file} done.')

# compile all the data into a single dataframe, using the prev. generated list as data
df = pd.concat(df_list, axis=0, ignore_index=True)

# count the number of entries for each drive model
model_counts = df['model'].value_counts()
print(f'Here are a list of the model choices for analysis: {model_counts}. \nThere are {len(model_counts)} total drive models available.')

# TODO we should allow the user to input the model number of the drive to look at drive specific data
# filter for only the specific drive the user cares about
drive_model_of_interest = input("Enter the exact model number (e.g. 'HGST HUH721212ALE600'): ")
specific_drive_filt = df['model'] == drive_model_of_interest
df = df[specific_drive_filt]

# get rid of all drives with < 1000 drive days
low_drive_day_filter = df['model'].value_counts().loc[lambda x: x < 1000]
drive_counts_df = low_drive_day_filter.to_frame()
filter_list = list(drive_counts_df.index)
new_filter = df['model'].isin(filter_list)
df = df[~new_filter]

# change the units for capacity to gbytes instead of bytes
df['capacity_bytes'] = pd.to_numeric(df['capacity_bytes'], downcast='float')
df['capacity_bytes'] = df['capacity_bytes'] / 1_000_000_000
# rename the capacity column accordingly
df.rename(columns={'capacity_bytes': 'capacity_gbytes'}, inplace=True)
# rename the smart 9 col to make the units more clear
df.rename(columns={'smart_9_raw': 'smart_9_raw (hours)'}, inplace=True)

# typecast the failures column (0 or 1) as a float so we can do a comparison
df['failure'] = pd.to_numeric(df['failure'], downcast='float')

# take all hours counts greater than 90k and make them their own data frame, then drop them (see filters)
# 90k hrs is ~10yrs, which is longer than any drive should have been in service
filt = df['smart_9_raw (hours)'] >= 90_000
indexNames = df[filt].index
df.drop(indexNames, inplace=True)

# count up the number of failures
num_failures = df['failure'].value_counts()
failed_drives = num_failures.loc[1]
# compute the daily failure rate = number of drive failures / total drive days (rows)
DFR = round((failed_drives / len(df)) * 100, 4)
print('Drive Days: ', len(df))

# compute the maximum power on hours of all drives
print(f'Maximum power on hours = {df["smart_9_raw (hours)"].max():,}')

# select (filter) only the failures (a failed drive has a '1' in this column)
failures = (df[df.failure >= 1])

# print some interesting statistics about the drives
print(f'Maximum hours at failure = {failures["smart_9_raw (hours)"].max():,}')
print(f'Minimum hours at failure = {failures["smart_9_raw (hours)"].min():,}')
print(f'Average hours at failure = {failures["smart_9_raw (hours)"].mean():,}')
print(f'Total number of drive failures: {failed_drives}')
print(f'Daily failure rate (DFR, %) =  {DFR}')
print(f'Annual failure rate (AFR, %) =  {DFR * 365}')

# print(df.head())
