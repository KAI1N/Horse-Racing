import numpy as np
import pandas as pd
import os
import tables
from fractions import Fraction
import re
import time
import matplotlib.pyplot as plt

start_time=time.time()
df = pd.read_csv('2010_2023_processed_data.csv')
'''
df['top3'] = (df['rank'] <= 3).astype(int)
df['win'] = (df['rank'] == 1).astype(int)
df['n_race'] = 0
df['n_race'] = df.groupby('name')['name'].transform('count')

df['win_rate'] = df.groupby('name')['win'].transform('mean')
df['top_3_rate'] = df.groupby('name')['top3'].transform('mean')

df.to_csv('2010_2023_processed_data.csv', index=False, encoding='utf-8')
'''
print(df.head())