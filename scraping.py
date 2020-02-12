import requests
from bs4 import BeautifulSoup
import urllib.request
import time

def scraping(url, max_page_num):
    # ページネーション実装
    page_list = get_page_list(url, max_page_num)
    # 画像URLリスト取得
    all_img_src_list = []
    for page in page_list:
        img_src_list = get_img_src_list(page)
        all_img_src_list.extend(img_src_list)
    return all_img_src_list


def get_img_src_list(url):
    # 検索結果ページにアクセス
    response = requests.get(url)
    # レスポンスをパース
    soup = BeautifulSoup(response.text, 'html.parser')
    img_src_list = [img.get('src') for img in soup.select('p.tb img')]
    return img_src_list


def get_page_list(url, max_page_num):
    img_num_per_page = 20
    page_list = [f'{url}{i*img_num_per_page+1}' for i in range(max_page_num)]
    return page_list

def download_img(src, dist_path):
    time.sleep(1)
    with urllib.request.urlopen(src) as data:
        img = data.read()
        with open(dist_path, 'wb') as f:
            f.write(img)
        
    
def main():
    url = "https://search.yahoo.co.jp/image/search?p=%E6%A9%8B%E6%9C%AC%E7%92%B0%E5%A5%88&ei=UTF-8&b="
    MAX_PAGE_NUM = 1
    all_img_src_list = scraping(url, MAX_PAGE_NUM)
    
    # 画像ダウンロード
    for i, src in enumerate(all_img_src_list):
        download_img(src, f'./img/kanna_{i}.jpg')


if __name__ == '__main__':
    main()
