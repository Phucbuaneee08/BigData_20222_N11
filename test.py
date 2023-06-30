import requests
from bs4 import BeautifulSoup
import re 

results = []

res = requests.get('https://thuvienphapluat.vn/hoi-dap-phap-luat/bat-dong-san?page=1')
soup = BeautifulSoup(res.content, 'html.parser')
element = soup.select('.news-card')

for e in element:
    question = e.find('a')
    link_answer = question['href']
    print(link_answer)
    keywords = []
    keyword = e.select('.keyword')
    for k in keyword:
        keywords.append(k.text)
    
