import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import os

html=open('html/2020/202001010101.html',encoding='utf-8')
html_content=html.read()
soup=BeautifulSoup(html_content,'html.parser')
text = soup.find_all('span')
text=text[7].text
parts = [part.strip().replace('天候 : ', '').replace('芝 : ', '').replace('ダート : ','').replace('発走 : ', '') for part in text.split('/')]
ground=parts[0][:1]
rotation=parts[0][1]
length=parts[0][2:]
wether=parts[1]
ground_condtion=parts[2]
start_time=parts[3]
print(ground_condtion)