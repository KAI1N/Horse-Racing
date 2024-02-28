import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import os
import requests
import time


data=[]
unique_horse_ids = set()
start_year=2010
end_year=2023

for year in range(start_year,end_year+1):
    save_dir = "html"+"/"+str(year)
    with open('txt'+'/'+str(year)+".txt", "r",encoding='utf-8') as f:
        urls = f.read().splitlines()
        for url in urls:
            list = url.split("/")
            race_id = list[-2]
            html=open(save_dir+"/"+race_id+'.html',encoding='utf-8')
            html_content=html.read()
            soup=BeautifulSoup(html_content,'html.parser')
            tag_tr=soup.find_all('tr')
            for i in range(1,17):
                try:
                    tag_td=tag_tr[i].find_all('td')
                    name_place=tag_td[3]
                    name=name_place.text.replace('\n','')
                    horse_id=name_place.find('a')['href'].split('/')[2]
                    if horse_id in unique_horse_ids:
                        continue
                    unique_horse_ids.add(horse_id)
                    url='https://db.netkeiba.com/horse/ped/'+str(horse_id)+'/'
                    response = requests.get(url)
                    response.encoding = response.apparent_encoding
                    html = response.text
                    horse_soup=BeautifulSoup(html,'html.parser')
                    father=horse_soup.find('td',rowspan='16',class_='b_ml').find('a').text.replace('\n','').replace(' ','')
                    grand_father_1=horse_soup.find_all('td',rowspan='8',class_='b_ml')[0].find('a').text.replace('\n','').replace(' ','')
                    grand_father_2=horse_soup.find_all('td',rowspan='8',class_='b_ml')[1].find('a').text.replace('\n','').replace(' ','')
                    mother=horse_soup.find('td',rowspan='16',class_='b_fml').find('a').text.replace('\n','').replace(' ','')
                    grand_mother_1=horse_soup.find_all('td',rowspan='8',class_='b_fml')[0].find('a').text.replace('\n','').replace(' ','')
                    grand_mother_2=horse_soup.find_all('td',rowspan='8',class_='b_fml')[1].find('a').text.replace('\n','').replace(' ','')
                    row=[name,horse_id,father,mother,grand_father_1,grand_father_2,grand_mother_1,grand_mother_2]
                    data.append(row)
                except:
                    break

df=pd.DataFrame(data,columns=['name','father','mother','grand_father_1','grand_father_2','grand_mother_1','grand_mother_2'])
filename = 'horse_relative_data'+str(start_year)+'_to_'+str(end_year)+'.csv'
df.to_csv(filename, index=False, encoding='utf-8')
print('finished successfully')