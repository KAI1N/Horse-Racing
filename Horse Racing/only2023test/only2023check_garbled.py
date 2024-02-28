import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import os
import requests
import time

def is_japanese(char):
    # Checks if character is within common Japanese ranges
    return any([
        0x3000 <= ord(char) <= 0x303F,  # Punctuation
        0x3040 <= ord(char) <= 0x309F,  # Hiragana
        0x30A0 <= ord(char) <= 0x30FF,  # Katakana
        0x4E00 <= ord(char) <= 0x9FFF,  # Common Kanji
        # Add more ranges as necessary
    ])

df = pd.read_csv('race_data2023_to_2023.csv',encoding='utf-8')
year=2023
save_dir="html"+"/"+str(year)
race_id=0

for row in range(df.shape[0]):
    for char in df.iloc[row]['name']:
        if not is_japanese(char):
##
            if not race_id==df.iloc[row]['race_id']:
                save_file_path = save_dir+"/"+str(df.iloc[row]['race_id'])+'.html'
                response = requests.get('https://db.netkeiba.com/race/'+str(df.iloc[row]['race_id'])+'/')
                response.encoding = response.apparent_encoding
                html = response.text
                time.sleep(3)
                with open(save_file_path, 'w',encoding='utf-8') as file:
                    file.write(html)
                race_id=df.iloc[row]['race_id']
                html=open(save_dir+"/"+str(race_id)+'.html',encoding='utf-8')
                html_content=html.read()
                soup=BeautifulSoup(html_content,'html.parser')
                tag_span = soup.find_all('span')
                tag_tr=soup.find_all('tr')
                for i in range(1,17):
                    try:
                        text=tag_span[7].text
                        parts = [part.strip().replace('天候 : ', '').replace('芝 : ', '').replace('ダート : ', '').replace('発走 : ', '') for part in text.split('/')]
                        ground=parts[0][:1]
                        tag_td=tag_tr[i].find_all('td')
                        name=tag_td[3].text.replace('\n','')
                        sex_age=tag_td[4].text
                        e_weight=tag_td[5].text
                        jockey=tag_td[6].text.replace('\n','')
                        time=tag_td[7].text
                        gap=tag_td[8].text
                        p_rank=tag_td[10].text
                        acsent=tag_td[11].text
                        odds=tag_td[12].text
                        pop=tag_td[13].text
                        h_weight=tag_td[14].text
                        rotation=parts[0][1]
                        length=parts[0][2:]
                        weather=parts[1]
                        ground_condition=parts[2]
                        start_time=parts[3]
                        df.loc[row]=[year,df.iloc[row]['race_id'],ground,rotation,length,weather,ground_condition,start_time,i,name,sex_age,e_weight,jockey,gap,p_rank,acsent,odds,pop,h_weight]
            
                    except:
                        break
                break
        else:
            break
df.to_csv('race_data2023_to_2023.csv', index=False, encoding='utf-8')
for row in range(df.shape[0]):
    for char in df.iloc[row]['name']:
        if not is_japanese(char):
            print(f"Is garbled {row}: {df.iloc[row]['race_id']}")
        else:
            break
'''
for row in range(df.shape[0]):
    for char in df.iloc[row]['name']:
        if not is_japanese(char):
            print(f"Is garbled {row}: {df.iloc[row]['race_id']}")
##
            i=df.iloc[row]['rank']
            html=open(save_dir+"/"+str(df.iloc[row]['race_id'])+'.html',encoding='utf-8')
            html_content=html.read()
            soup=BeautifulSoup(html_content,'html.parser')
            tag_span = soup.find_all('span')
            tag_tr=soup.find_all('tr')
            text=tag_span[7].text
            parts = [part.strip().replace('天候 : ', '').replace('芝 : ', '').replace('ダート : ', '').replace('発走 : ', '') for part in text.split('/')]
            ground=parts[0][:1]
            tag_td=tag_tr[i].find_all('td')
            name=tag_td[3].text.replace('\n','')
            sex_age=tag_td[4].text
            e_weight=tag_td[5].text
            jockey=tag_td[6].text.replace('\n','')
            time=tag_td[7].text
            gap=tag_td[8].text
            p_rank=tag_td[10].text
            acsent=tag_td[11].text
            odds=tag_td[12].text
            pop=tag_td[13].text
            h_weight=tag_td[14].text
            rotation=parts[0][1]
            length=parts[0][2:]
            weather=parts[1]
            ground_condition=parts[2]
            start_time=parts[3]
            df.loc[df.iloc[row]['race_id']]=[year,df.iloc[row]['race_id'],ground,rotation,length,weather,ground_condition,start_time,i,name,sex_age,e_weight,jockey,gap,p_rank,acsent,odds,pop,h_weight]
            ##
            print(df.iloc[row])
            break
        else:
            break
'''