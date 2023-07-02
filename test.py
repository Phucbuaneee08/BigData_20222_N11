import requests
from bs4 import BeautifulSoup
import re 

results = []

def remove_html_tags(text):
    soup = BeautifulSoup(text, 'html.parser')
    return soup.get_text()

res = requests.get('https://thuvienphapluat.vn/hoi-dap-phap-luat/839CEF7-hd-giao-vien-thuoc-doi-tuong-duoc-thue-nha-cong-vu-khong.html')
soup = BeautifulSoup(res.text, 'html.parser')
elements = soup.select('.news-content')
html = str(elements)
html = remove_html_tags(html)
html = html.replace("\n", "")
html = html.replace("\r", "")
html = html.replace("  ", "")
print(html.strip())


    
