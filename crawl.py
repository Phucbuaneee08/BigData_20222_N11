import requests
from bs4 import BeautifulSoup
import re
import json
import threading

def process_page(page):
    results = []
    base_link = 'https://thuvienphapluat.vn/hoi-dap-phap-luat/bat-dong-san?page='
    res = requests.get(base_link + str(page))
    soup = BeautifulSoup(res.content, 'html.parser')
    element = soup.select('.news-card')

    for e in element:
        question = e.find('a')
        keywords = []
        keyword = e.select('.keyword > a')
        for k in keyword:
            keywords.append(k['title'])
        link_answer = question['href']
        res2 = requests.get(link_answer)
        soup2 = BeautifulSoup(res2.content, 'html.parser')
        questions = soup2.select('p')
        answer = '' 
        for i in questions:
            if re.search(r'Như vậy', i.text):
                answer = i.text
                break

        results.append({'question': question['title'], 'answer': answer, 'keywords': keywords})
    return results

    # return results
    # questions = soup.select('.news-card > a')
    
    # for question in questions:
    #     link_answer = question['href']
    #     res2 = requests.get(link_answer)
    #     soup2 = BeautifulSoup(res2.content, 'html.parser')

    #     questions = soup2.select('p')
    #     answer = '' 
    #     for i in questions:
    #         if re.search(r'Như vậy', i.text):
    #             answer = i.text
    #             break

    #     results.append({'question': question['title'], 'answer': answer})

    # return results

def main():
    threads = []
    num_pages = 400
    num_threads = 6  # Số luồng mong muốn

    # Tạo một Lock để đồng bộ hóa việc ghi file
    file_lock = threading.Lock()

    for i in range(1, 400):  # Bắt đầu từ trang thứ 1
        thread = threading.Thread(target=lambda page=i: save_page_results(page, file_lock))
        thread.start()
        threads.append(thread)

        # Điều chỉnh số lượng luồng nếu vượt quá giới hạn
        if len(threads) >= num_threads:
            for thread in threads:
                thread.join()
            threads = []

    for thread in threads:
        thread.join()

    print("Loading...100%  DONE")

def save_page_results(page, file_lock):
    results = process_page(page)
    file_name = f'data_page{page}.json'
    with open(file_name, 'w', encoding='utf-8') as file:
        # Sử dụng Lock để đảm bảo chỉ có một luồng ghi file tại một thời điểm
        file_lock.acquire()
        json.dump(results, file, ensure_ascii=False, indent=4)
        file_lock.release()
    print("Cloning Page "+ str(page)+" Successfully")

if __name__ == "__main__":
    main()
