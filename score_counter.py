#imports

from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#settings
url='https://lk.msu.ru/cabinet'

opts = webdriver.ChromeOptions()
opts.add_argument("--headless")
driver = webdriver.Chrome(options=opts)
driver.get(url)

#login tag settings
tag_id = driver.find_element(By.NAME,'LoginForm[email]')
tag_pw = driver.find_element(By.NAME,"LoginForm[password]")
tag_lg_button=driver.find_element(By.NAME,'login-button')

#login

#inputs
id_= "songheelee2810@gmail.com"
pw = "songhee2002"
tag_id.send_keys(id_)
tag_pw.send_keys(pw)
tag_lg_button.click()

tag_pt = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.LINK_TEXT, "Оценки"))
)
tag_pt.click()

#parse the score page
soup=driver.page_source
soup=bs(soup,'html.parser')

#pop only text-success classes
tr=list(soup.find_all('tr'))
successes=[]
for tag in tr:
    # successes.append(tag)
    if "text-success" in str(tag):
        successes.append(tag)

#score counts
pt_sum_5=0
pt_sum_4_5=0
pt_sum_4_3=0
pt_count=0
for tag in successes:
    if 'удов.' in str(tag):
        pt_count+=1
        pt_sum_5+=3
        pt_sum_4_5+=2.7
        pt_sum_4_3+=2.58
    elif 'хорошо' in str(tag):
        pt_count+=1
        pt_sum_5+=4
        pt_sum_4_5+=3.6
        pt_sum_4_3+=3.44
    elif 'отлично' in str(tag):
        pt_count+=1
        pt_sum_5+=5
        pt_sum_4_5+=4.5
        pt_sum_4_3+=4.3
    elif 'не сдано' in str(tag):
        pt_count+=1
        pt_sum_5+=2
        pt_sum_4_5+=1.72
        pt_sum_4_3+=1.8
    else:
        continue

#printing results
print(round(pt_sum_5/pt_count,2),'/ 5.0')
print(round(pt_sum_4_5/pt_count,2),'/ 4.5')
print(round(pt_sum_4_3/pt_count,2),'/ 4.3')