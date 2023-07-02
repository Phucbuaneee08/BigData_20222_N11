import requests
from bs4 import BeautifulSoup
import re
import json
import threading

def remove_html_tags(text):
    soup = BeautifulSoup(text, 'html.parser')
    return soup.get_text()

def process_page(page):
    results = []
    base_link = 'https://thuvienphapluat.vn/hoi-dap-phap-luat/bat-dong-san?page='
    res = requests.get(base_link + str(page))
    soup = BeautifulSoup(res.content, 'html.parser')
    element = soup.select('.news-card')

    if not element:
        return results  # Kết thúc nếu không có dữ liệu trên trang

    for e in element:
        question = e.find('a')
        keywords = []
        keyword = e.select('.keyword > a')
        for k in keyword:
            keywords.append(k['title'])
        link_answer = question['href']
        res2 = requests.get(link_answer)
        soup2 = BeautifulSoup(res2.text, 'html.parser')
        answer = soup2.select('.news-content')
        answer = str(answer)
        answer = remove_html_tags(answer)
        answer = answer.replace("\n", "")
        answer = answer.replace("  ", "")
        answer = answer.replace("\r", "")
        results.append({'question': question['title'], 'answer': answer, 'keywords': keywords})
    return results

def main():
    num_threads = 6  # Số luồng mong muốn

    # Tạo một Lock để đồng bộ hóa việc ghi file
    file_lock = threading.Lock()

    page = 1  # Bắt đầu từ trang đầu tiên
    while True:
        threads = []

        results = process_page(page)

        if not results:
            break  # Kết thúc nếu không có dữ liệu trên trang

        thread = threading.Thread(target=lambda page=page: save_page_results(page, results, file_lock))
        thread.start()
        threads.append(thread)

        page += 1

        # Điều chỉnh số lượng luồng nếu vượt quá giới hạn
        if len(threads) >= num_threads:
            for thread in threads:
                thread.join()
            threads = []

    for thread in threads:
        thread.join()

    print("Crawling completed.")

def save_page_results(page, results, file_lock):
    file_name = f'data_page{page}.json'
    with open(file_name, 'w', encoding='utf-8') as file:
        # Sử dụng Lock để đảm bảo chỉ có một luồng ghi file tại một thời điểm
        file_lock.acquire()
        json.dump(results, file, ensure_ascii=False, indent=4)
        file_lock.release()
    print("Crawling Page " + str(page) + " Successfully")

if __name__ == "__main__":
    main()
