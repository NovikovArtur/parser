import time
import requests
from selenium import webdriver as wd
import csv
from selenium.webdriver.common.by import By
import os


def is_file_empty(filepath):
    return os.stat(filepath).st_size == 0


st_accept = "text/html"
st_useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
headers = {
   "Accept": st_accept,
   "User-Agent": st_useragent
}
req = requests.get("https://ok.ru/feed", headers)
src = req.text
login = "89154428502"
password = "hiZopOx3"
browser = wd.Chrome()
browser.get("https://ok.ru/feed")
time.sleep(7)
login_block = browser.find_element(By.XPATH, "/html/body/div[11]/div[5]/div[2]/div[1]/div/div/div/div[2]/div[3]/div[4]/div/div/main/div/div/div/div[2]/div[2]/div/div[2]/div[2]/div[1]/form/div[1]/div/input")
login_block.send_keys(login)
time.sleep(2)
password_block = browser.find_element(By.XPATH, "/html/body/div[11]/div[5]/div[2]/div[1]/div/div/div/div[2]/div[3]/div[4]/div/div/main/div/div/div/div[2]/div[2]/div/div[2]/div[2]/div[1]/form/div[2]/div/input")
password_block.send_keys(password)
time.sleep(1)
browser.find_element(By.XPATH, "/html/body/div[11]/div[5]/div[2]/div[1]/div/div/div/div[2]/div[3]/div[4]/div/div/main/div/div/div/div[2]/div[2]/div/div[2]/div[2]/div[1]/form/div[4]/input").click()
time.sleep(5)


with open("GroupsOK.csv", newline='', encoding='utf-8') as Groups:
    reader = csv.reader(Groups, delimiter=';')
    community_ids = []
    for row in reader:
        community_ids.append(row[0])
    print("Получили данные о всех группах, приступаю к поиску")


posts_file = 'posts2.csv'


with open(posts_file, mode='a', newline='', encoding='utf-8') as posts:
    writer_posts = csv.writer(posts)
    if is_file_empty(posts_file):
        writer_posts.writerow(['community_id', 'count_posts', 'count_comments', 'count_likes',
                               'count_hrefs', 'count_keywords'])
    for count in range(100, 191):
        if 'community_id' not in community_ids[count]:
            print(f"начинаем парсинг {count} группы")
            href = "https://ok.ru/group/" + community_ids[count]
            browser.get(href)
            for i in range(15):
                browser.execute_script("window.scrollBy(0, 100000);")
                time.sleep(5)
            try:
                browser.find_element(By.CSS_SELECTOR, '.loader-controls.loader-controls-bottom').click()
            except:
                pass
            date = browser.find_elements(By.CSS_SELECTOR, '.feed-info-date.feed-info-subtitle_i')
            while ('2023' not in date[-1].text) and ('2022' not in date[-1].text) and ('2021' not in date[-1].text) and ('2020' not in date[-1].text):
                for i in range(15):
                    browser.execute_script("window.scrollBy(0, 100000);")
                    time.sleep(2)
                time.sleep(5)
                try:
                    browser.find_element(By.CSS_SELECTOR, '.loader-controls.loader-controls-bottom').click()
                except:
                    break
                date = browser.find_elements(By.CSS_SELECTOR, '.feed-info-date.feed-info-subtitle_i')
            print("Получили информацию, начинаем обработку")
            check_first_post = 0
            if ('2023' not in str(date[0].text) and '2022' not in str(date[0].text) and '2021' not in
                    str(date[0].text) and '2020' not in str(date[0].text)):
                check_first_post = 1
            new_date = [i for i in date if
                        '2023' not in str(i.text) and '2022' not in str(i.text) and '2021' not in str(
                            i.text) and '2020' not in str(i.text)]
            date = new_date
            count_posts = len(date)
            all_count = browser.find_elements(By.CSS_SELECTOR, '.feed_f')
            if check_first_post == 1:
                all_count = all_count[0:count_posts]
            else:
                all_count = all_count[1:count_posts + 1]
            count_comments = 0
            count_likes = 0
            for i in all_count:
                text = str(i.text)
                lines = text.split('\n')
                try:
                    count_likes += int(lines[0].split(' ')[0])
                except:
                    pass
                try:
                    count_comments += int(lines[2])
                except:
                    pass
            keywords = ["Ваканс", "Ищете работу", "Ищите работу", "Найти работу",
                        "Вакансии", "Ищу работу", "Вакансий", "Приглашаем на работу",
                        "Работа вахтой", "Требуется", "Прямой работодатель",
                        "Дружный коллектив", "открыт набор", "Работ", "работ", 'ваканс', 'треб',
                        "резюме", 'заработная', 'зп', 'оплата', 'зарплата']
            all_texts = browser.find_elements(By.CSS_SELECTOR, '.media-block.media-text.h-mod.__without-margin')
            if check_first_post == 1:
                all_texts = all_texts[0:count_posts]
            else:
                all_texts = all_texts[1:count_posts + 1]
            count_hrefs = 0
            count_keywords = 0
            for i in all_texts:
                text = str(i.text)
                if ('hhtp' in text) or ('https' in text):
                    count_hrefs += 1
                for keyword in keywords:
                    if keyword in text:
                        count_keywords += 1
            print(community_ids[count], count_posts, count_comments, count_likes, count_hrefs, count_keywords)
            writer_posts.writerow([community_ids[count], count_posts, count_comments, count_likes,
                                   count_hrefs, count_keywords])
            time.sleep(5)

print("Обработка завершена")
