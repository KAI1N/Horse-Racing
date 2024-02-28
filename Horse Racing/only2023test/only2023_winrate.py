import numpy as np
import pandas as pd
import os
import tables

horse_df = pd.read_csv('race_data_2023_to_2023.csv')
relative_df = pd.read_csv('horse_relative_data_2023_to_2023.csv')

df = horse_df.merge(relative_df, on='name', how='left')

df['top3'] = (df['rank'] <= 3).astype(int)
df['win'] = (df['rank'] == 1).astype(int)
df['n_race'] = 0
df['n_race'] = df.groupby('name')['n_race'].transform('count')

mean_rank_1 = df.groupby('name')['win'].mean()
mean_rank_3 = df.groupby('name')['top3'].mean()

print(df)
print(mean_rank_1)
print(mean_rank_3)
