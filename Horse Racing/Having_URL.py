import time
import os

from selenium import webdriver
from selenium.webdriver.support.ui import Select,WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

#selenium 3.141.0
#chrome 120.0.6099.217
#chrome driver same

options = Options()
options.add_argument('--headless')    # ヘッドレスモードに
driver = webdriver.Chrome("C:/Users/khata/OneDrive/デスクトップ/Horse Racing/chromedriver-win32/chromedriver.exe") 
wait = WebDriverWait(driver,10)

#full success

#年の設定
#1975,1976でやると途中で終わってしまう
#1975only->success
#たまにうまくいかなくなる
#2000から2013までやった結果、なぜか2004年の最後にerrorが起きた。インターネットのせいかも
start_year=1991
end_year=1994

#file名に年を入れたいので、年ごとにサーチ
for year in range(start_year,end_year+1):
    URL = "https://db.netkeiba.com/?pid=race_search_detail"
    driver.get(URL)
    time.sleep(1)
    wait.until(EC.presence_of_all_elements_located)

    #monthを1～12までやってみる->fail
    #monthを2~3までやってみる->success
    #monthを4~12まで→100までkillcomad
    #monthを4～6->success
    #monthを7~12->success
    #多分、chrome開いてなかったから？->たぶんそう
    #year2020,1~12->all success

    #月の設定
    start_month=1
    end_month=12


    #期間の設定
    start_year_element = driver.find_element_by_name('start_year')
    start_year_select = Select(start_year_element)
    start_year_select.select_by_value(str(year))
    start_mon_element = driver.find_element_by_name('start_mon')
    start_mon_select = Select(start_mon_element)
    start_mon_select.select_by_value(str(start_month))
    end_year_element = driver.find_element_by_name('end_year')
    end_year_select = Select(end_year_element)
    end_year_select.select_by_value(str(year))
    end_mon_element = driver.find_element_by_name('end_mon')
    end_mon_select = Select(end_mon_element)
    end_mon_select.select_by_value(str(end_month))

    #グランドの設定
    for i in range(1,3):
        terms = driver.find_element_by_id("check_track_"+ str(i))
        terms.click()

    #競馬場の設定
    for i in range(1,11):
        terms = driver.find_element_by_id("check_Jyo_"+ str(i).zfill(2))
        terms.click()

    # 表示件数を選択(20,50,100の中から最大の100へ)
    list_element = driver.find_element_by_name('list')
    list_select = Select(list_element)
    list_select.select_by_value("100")

    # フォームを送信
    frm = driver.find_element_by_css_selector("#db_search_detail_form > form")
    frm.submit()
    time.sleep(5)
    wait.until(EC.presence_of_all_elements_located)

    #making files for each year
    save_dir = "txt"
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)

    with open(save_dir+'/'+str(year)+".txt", mode='w') as f:
        while True:
            time.sleep(5)
            wait.until(EC.presence_of_all_elements_located)
            all_rows = driver.find_element_by_class_name('race_table_01').find_elements_by_tag_name("tr")
            for row in range(1, len(all_rows)):
                race_href=all_rows[row].find_elements_by_tag_name("td")[4].find_element_by_tag_name("a").get_attribute("href")
                f.write(race_href+"\n")
            try:
                target = driver.find_elements_by_link_text("次")[0]
                driver.execute_script("arguments[0].click();", target) #javascriptでクリック処理
            except IndexError:
                break  