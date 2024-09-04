import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import requests
import re

from src.scrapper.inscrawler import InsCrawler


class InsDataCrawler(InsCrawler):
    def __init__(self,
                 driver, data,
                 dev: bool = False):
        super().__init__(dev=dev, driver=driver)
        self.data = data
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
        }

    def get_post_data(self):
        results = f'{self.base_path}/results/data.txt'
        with open(results, 'r') as f:
            post_crawled_data = {line.strip() for line in f}

        for idx, (key, val) in enumerate(self.data.items()):

            post_url = val.post_url

            if post_url in post_crawled_data:
                continue

            self.driver.get(post_url)
            print(idx, '. ' + post_url)

            try:
                time.sleep(5)
                html = self.driver.page_source
                soup = BeautifulSoup(html, 'lxml')

                # 작성자
                username = soup.find('span', {'class': '_ap3a _aaco _aacw _aacx _aad7 _aade'}).text
                print(username, end=' ')
                self.data[key].username = username

                # 작성일자
                date = soup.find_all('time')[-1]['datetime'][:10]
                print(date, end=' ')
                self.data[key].date = date

                # like 개수
                try:
                    like = soup.find('span', {'class': 'html-span xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1hl2dhg x16tdsg8 x1vvkbs'}).text
                except Exception:
                    like = 'no data'  # ~~외 여러 명이 좋아합니다. 같은 경우
                print(like)
                self.data[key].like = like

                # 이미지 저장
                images = []
                img_urls = set()
                images.append(self.driver.find_elements(By.CLASS_NAME, 'x5yr21d.xu96u03.x10l6tqk.x13vifvy.x87ps6o.xh8yej3'))

                for i in range(len(images)):
                    for j in range(len(images[i])):

                        if j >= 3:  # 4번째부터 타 게시물의 썸네일 이미지
                            break

                        alt = images[i][j].get_attribute('alt')
                        check = re.findall(r'by .+? on', alt)  # 타 게시물인지 아닌지 검사

                        if check != []:
                            img_urls.add(images[i][j].get_attribute('src'))

                # 이미지 끝까지 넘기면서 url 추출
                try:
                    while True:
                        time.sleep(3)

                        self.driver.find_element(By.CLASS_NAME, '_afxw._al46._al47').click()  # 다음 이미지 버튼 클릭
                        images.append(self.driver.find_elements(By.CLASS_NAME, 'x5yr21d.xu96u03.x10l6tqk.x13vifvy.x87ps6o.xh8yej3'))

                        for i in range(len(images)):
                            for j in range(len(images[i])):

                                if j >= 3:  # 4번째부터 타 게시물의 썸네일 이미지
                                    break

                                alt = images[i][j].get_attribute('alt')
                                check = re.findall(r'by .+? on', alt)  # 타 게시물인지 아닌지 검사

                                if check != []:
                                    img_urls.add(images[i][j].get_attribute('src'))

                        images.clear()

                except Exception:
                    print('더 이상 넘길 이미지 없음')

                    img_urls = list(img_urls)
                    print(img_urls)
                    images.clear()

                saved_imgs = set()
                for img_url in img_urls:
                    # 이미지만 고려. 우선 비디오 타입은 고려하지 않음.
                    pattern = r'\/v\/[^\/]+\/([^\/\?]+)\.(jpg|png|webp|heic)'
                    match = re.search(pattern, img_url)
                    if match:
                        img_name = match.group(1) + '.' + match.group(2)
                    else:
                        print('파일을 찾을 수 없거나 jpg 혹은 png, webp, heic 파일이 아님.')
                        continue

                    if img_name not in saved_imgs:
                        response = requests.get(img_url, headers=self.headers, timeout=20)

                        with open(f'{self.base_path}/results/images/' + img_name, 'wb') as f:
                            f.write(response.content)

                        saved_imgs.add(img_name)

                    time.sleep(.5)

                print(f"총 {len(saved_imgs)} 장의 이미지 저장")
                self.data[key].saved_imgs = str(list(saved_imgs))

                time.sleep(5)

            except Exception as e:
                print(e)
                print('오류 발생')

        # 수집 완료된 데이터 키값(post url unique id) 저장
        with open(results, 'a') as f:
            for key in self.data.keys():
                f.write(key + '\n')

        self.driver.close()
