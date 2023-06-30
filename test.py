import requests
from bs4 import BeautifulSoup
import re 

results = []

res = requests.get('https://thuvienphapluat.vn/hoi-dap-phap-luat/839CE5A-hd-dat-phi-nong-nghiep-khac-co-xay-nha-o-duoc-khong.html')
soup = BeautifulSoup(res.content, 'html.parser')
questions = soup.select('p')


for i in questions:
    if re.search(r'Như vậy',i.text):
        print(i.text)

