import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import os
import requests
import time
import check_grabled_html

starttime= time.time()
data=[]

#ここをいじる
start_year=2010
end_year=2023

for year in range(start_year,end_year+1):
    save_dir = "html"+"/"+str(year)
    with open('txt'+'/'+str(year)+".txt", "r",encoding='utf-8') as f:
        urls = f.read().splitlines()
        for url in urls:
            try:
                list = url.split("/")
                race_id = list[-2]
                html = open(save_dir+"/"+race_id+'.html',encoding='utf-8')
                html_content = html.read()
                soup = BeautifulSoup(html_content,'html.parser')

                #ここからスクレイピング
                #表のデータの取得
                tag_span = soup.find_all('span')

                #出走のデータの取得
                tag_tr = soup.find_all('tr')
                text = tag_span[6].text

                #tag_span[7]のものもあるみたい？->[7]の方が多い圧倒的に。競輪の関係のやつかも
                if text=='LIVE':
                    text = tag_span[7].text
                
                #trの邪魔なものを消去
                parts = [part.strip().replace('天候 : ', '').replace('芝 : ', '').replace('ダート : ', '').replace('発走 : ', '') for part in text.split('/')]

                #表のデータの取得
                tag_table = soup.find_all('table',summary='払い戻し')   
                table_1 = tag_table[0].find_all('tr')
                table_2 = tag_table[1].find_all('tr')


                #高速化により、変わらないものを上に
                #出走データ
                ground = parts[0][:1]
                rotation = parts[0][1]
                length = parts[0][2:]
                weather = parts[1]
                ground_condition = parts[2]
                start_time = parts[3]

                #払い戻しデータ
                tan = table_1[0].find('td',class_="txt_r").text
                try:
                    fuku_1 = table_1[1].find('td',class_="txt_r").decode_contents().split('<br/>')[0]
                    fuku_2 = table_1[1].find('td',class_="txt_r").decode_contents().split('<br/>')[1]
                    fuku_3 = table_1[1].find('td',class_="txt_r").decode_contents().split('<br/>')[2]
                    uren = table_1[3].find('td',class_="txt_r").text
                except:
                    fuku_1 = table_1[1].find('td',class_="txt_r").decode_contents().split('<br/>')[0]
                    fuku_2 = table_1[1].find('td',class_="txt_r").decode_contents().split('<br/>')[1]
                    fuku_3 = np.NaN
                    uren = table_1[2].find('td',class_="txt_r").text
                wide_1_2 = table_2[0].find('td',class_="txt_r").decode_contents().split('<br/>')[0]
                wide_1_3 = table_2[0].find('td',class_="txt_r").decode_contents().split('<br/>')[1]
                wide_2_3 = table_2[0].find('td',class_="txt_r").decode_contents().split('<br/>')[2]
                utan = table_2[1].find('td',class_="txt_r").text
                sanfuku = table_2[2].find('td',class_="txt_r").text
                santan = table_2[3].find('td',class_="txt_r").text

                for i in range(1,17):
                    #16個じゃないものがあるため、tryを用いた
                    try:
                        #span
                        tag_td = tag_tr[i].find_all('td')
                        name = tag_td[3].text.replace('\n','')
                        sex_age = tag_td[4].text
                        e_weight = tag_td[5].text
                        jockey = tag_td[6].text.replace('\n','')
                        t = tag_td[7].text
                        gap = tag_td[8].text
                        p_rank = tag_td[10].text
                        acsent = tag_td[11].text
                        odds = tag_td[12].text
                        pop = tag_td[13].text
                        h_weight = tag_td[14].text

                        #所得したものを合併
                        row = [year,race_id,ground,rotation,length,weather,ground_condition,start_time,tan,fuku_1,fuku_2,fuku_3,uren,wide_1_2,wide_1_3,wide_2_3,utan,sanfuku,santan,i,name,sex_age,e_weight,jockey,t,gap,p_rank,acsent,odds,pop,h_weight]
                        data.append(row)
                    except:
                        break
            except:
                print(url)
                continue


df=pd.DataFrame(data,columns=['year','race_id','ground','rotation','length','weather','ground_condition','start_time','tan','fuku_1','fuku_2','fuku_3','uren','wide_1_2','wide_1_3','wide_2_3','utan','sanfuku','santan','rank','name','sex_age','e_weight','jockey','time','gap','p_rank','acsent','odds','pop','h_weight'])
filename = 'race_data_'+str(start_year)+'_to_'+str(end_year)+'.csv'

# Save the DataFrame to a CSV file
df.to_csv(filename, index=False, encoding='utf-8')

end_time=time.time()
print((end_time - starttime)/60)
