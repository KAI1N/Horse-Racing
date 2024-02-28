import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import os
import requests
import time

start_time=time.time()
#making_dataの流用
start_year=2010
end_year=2023

for year in range(start_year,end_year+1):
    save_dir = "html"+"/"+str(year)
    with open('txt'+'/'+str(year)+".txt", "r",encoding='utf-8') as f:
        urls = f.read().splitlines()
        for url in urls:

            list = url.split("/")
            race_id = list[-2]
            html = open(save_dir+"/"+race_id+'.html',encoding='utf-8')
            html_content = html.read()
            soup = BeautifulSoup(html_content,'html.parser')

            #表のデータの取得
            tag_table = soup.find_all('table',summary='払い戻し')

            #文字化けを処理するため
            if not len(tag_table) > 0:
                print(url)
                list = url.split("/")
                race_id = list[-2]
                save_file_path = save_dir+"/"+race_id+'.html'
                response = requests.get(url)
                response.encoding = response.apparent_encoding
                html = response.text
                with open(save_file_path, 'w',encoding='utf-8') as file:
                    file.write(html)
end_time=time.time()
print((end_time-start_time)/60)