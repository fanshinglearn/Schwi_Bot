import time
import requests
from requests.exceptions import ConnectionError, Timeout
from bs4 import BeautifulSoup

class Crawler:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    
    # # 如果哪天get_r()失敗再試試這個
    # def get_r(self, url, retries=3, backoff_factor=0.3):
    #     headers = {
    #         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    #     }
        
    #     for retry in range(retries):
    #         try:
    #             r = requests.get(url, headers=headers, timeout=10)
    #             r.raise_for_status()  # If the response was successful, no Exception will be raised
    #             return r
    #         except (ConnectionError, Timeout) as e:
    #             print(f"第 {retry + 1} 次嘗試失敗: {e}")
    #             time.sleep(backoff_factor * (2 ** retry))  # Exponential backoff
    #         except requests.exceptions.HTTPError as errh:
    #             print("HTTP 錯誤:", errh)
    #             break
    #         except requests.exceptions.RequestException as err:
    #             print("其他錯誤:", err)
    #             break
        
    #     raise ConnectionError(f"連接到 {url} 在重試 {retries} 次後失敗")
    
    @classmethod
    def get_r(cls, url):
        r = requests.get(url, headers=cls.headers)
        return r
    
    @classmethod
    def get_soup(cls, url):
        r = cls.get_r(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup

if __name__ == '__main__':
    pass
