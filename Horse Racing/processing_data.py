import numpy as np
import pandas as pd
import os
#rantime簡略化のため
import making_data as md

#df = pd.read_csv('race_data_2020_to_2023.csv')
#本当は上のようにやるかな
#データが多すぎるので、一番最新のもの（2023年）のものの運用をする。
#後々、すべての年についてやろうと思う。
import numpy as np
import pandas as pd
import os
import tables
from fractions import Fraction
import re
import time
#後で、processing_dataの方では可能な限り、分析できるようにする。
#rantime簡略化のため
#timeを加えたのでエラー出るかも

start_time=time.time()

df = pd.read_csv('race_data_2010_to_2023.csv')
#3位以内と3位以外のデータを同数にするために3位以外のものをランダムにドロップ

df['rank'] = pd.to_numeric(df['rank'])

ntop3 = df[df['rank'] > 3]
top3 = df[df['rank'] <= 3]

rows_to_drop = ntop3.sample(n=ntop3.shape[0]-top3.shape[0]).index
df_dropped = ntop3.drop(rows_to_drop)
df=pd.concat([top3, df_dropped], ignore_index=True)

#親戚についてのデータrelative_dfを取得、のちにベクトル変化したrelative_dataに変化するかも
#relative_df = pd.read_csv('horse_relative_data_2010_to_2023.csv')

#horse_idがいらない気がするので消去
#relative_df = relative_df[['name','father','mother','grand_father_1','grand_father_2','grand_mother_1','grand_mother_2']]


#障のものが存在するので、消去。
df = df[df['ground'] != '障']

#年の抽出。後々いるかも
df['year'] = df['race_id'].astype(str).str[:4]

#sex_ageからsexとageの抽出
df['age'] = df['sex_age'].astype(str).str[1:2]
df['sex'] = df['sex_age'].astype(str).str[:1]

#intにするため
df['length'] = df['length'].str.replace('m','')
df['length'] = df['length'].str.replace('線','')

#外というものが存在し、必要かどうかわからないが一応one-hot化
df['out_length'] = df['length'].apply(lambda x: 1 if '外' in x else 0)
df['length'] = df['length'].str.replace('外','')

#配当の,を消去
df['tan'] = df['tan'].str.replace(',','')
df['fuku_1'] = df['fuku_1'].str.replace(',','')
df['fuku_2'] = df['fuku_2'].str.replace(',','')
df['fuku_3'] = df['fuku_3'].str.replace(',','')
df['uren'] = df['uren'].str.replace(',','')
df['wide_1_2'] = df['wide_1_2'].str.replace(',','')
df['wide_1_3'] = df['wide_1_3'].str.replace(',','')
df['wide_2_3'] = df['wide_2_3'].str.replace(',','')
df['utan'] = df['utan'].str.replace(',','')
df['sanfuku'] = df['sanfuku'].str.replace(',','')
df['sanfuku'] = df['sanfuku'].str.replace(',','')

#カッコ内を抽出
df['weight_change'] = df['h_weight'].str.extract('\((.*?)\)')
df['h_weight'] = df['h_weight'].apply(lambda x: re.sub(r'\(.*?\)', '', x))
df['weight_change'] = df['weight_change'].str.replace('+','')

df['h_weight'] = df['h_weight'].str.replace('計不','')
df['odds'] = df['odds'].str.replace('---','')

#着差について、1馬身は2.4mなので、分数のものは2.4をかけた。ハナは20cm,アタマ40cm,クビ80cmに統一した
#着差について解読不能。例202304040405

#様々な変数のone-hot化
ground_dummies = pd.get_dummies(df['ground'])
weather_dummies = pd.get_dummies(df['weather'])
sex_dummies = pd.get_dummies(df['sex'])
rotation_dummies = pd.get_dummies(df['rotation'])
ground_condition_dummies = pd.get_dummies(df['ground_condition'])
jockey_dummies = pd.get_dummies(df['jockey']) 

#one-hot化したもの、綺麗にしたもの、追加したものなどがあるため、必要なだけにした。
horse_df = df[['length','out_length','name','age','e_weight','pop','h_weight','weight_change','rank','odds','tan','fuku_1','fuku_2','fuku_3','uren','wide_1_2','wide_1_3','wide_2_3','utan','sanfuku','santan']]

#one-hot化したものを合体
horse_df = pd.concat([horse_df, weather_dummies], axis=1)
horse_df = pd.concat([horse_df, ground_dummies], axis=1)
horse_df = pd.concat([horse_df, ground_condition_dummies], axis=1)
horse_df = pd.concat([horse_df, rotation_dummies], axis=1)
horse_df = pd.concat([horse_df, sex_dummies], axis=1)
horse_df = pd.concat([horse_df, jockey_dummies], axis=1)

#relative_dfも追加。のちにベクトルにするかも。
#result = horse_df.merge(relative_df, on='name', how='left')
#result['is_parents'] = result['name'].isin(result['father']) | result['name'].isin(result['mother'])
#result.to_csv('2023_processed_data.csv', index=False, encoding='utf-8')
horse_df.to_csv('2010_2023_processed_data.csv', index=False, encoding='utf-8')

end_time=time.time()

print(end_time-start_time)
