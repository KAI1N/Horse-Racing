import numpy as np
import pandas as pd
import os
import tables
from fractions import Fraction
import re
import time

start_time=time.time()
df = pd.read_csv('race_data_2023_to_2023.csv')
print(df[df['race_id']==202309050406])
end_time = time.time()
print(end_time - start_time)