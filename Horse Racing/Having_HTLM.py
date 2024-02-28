import os
import requests
import time

start_year=1995
end_year=1995

#たまに文字化ける
for year in range(start_year,end_year+1):
    save_dir = "html"+"/"+str(year)
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)


        '''
        文字化けが起きたのでテスト
        最後のopenにencodingを加えるのを忘れてた。
        with open(str(year)+"-"+str(month)+".txt", "r",encoding='utf-8') as f:
            urls = f.read().splitlines()
            url=urls[0]
            list = url.split("/")
            race_id = list[-2]
            save_file_path = save_dir+"/"+race_id+'.html'
            response = requests.get(url)
            response.encoding = response.apparent_encoding
            html = response.text
            time.sleep(5)
            with open(save_file_path, 'w',encoding='utf-8') as file:
                file.write(html)
        '''     
    with open("txt"+"/"+str(year)+".txt", "r",encoding='utf-8') as f:
        urls = f.read().splitlines()
        for url in urls:
            list = url.split("/")
            race_id = list[-2]
            save_file_path = save_dir+"/"+race_id+'.html'
            response = requests.get(url)
            response.encoding = response.apparent_encoding
            html = response.text
            time.sleep(3)
            with open(save_file_path, 'w',encoding='utf-8') as file:
                file.write(html)
