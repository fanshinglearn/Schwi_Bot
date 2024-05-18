import requests
from bs4 import BeautifulSoup

class TowerOfSaviors:
    def __init__(self):
        self.titles = []
        self.urls = []
        self.img_urls = []

    # 取得 標題 連結 圖片網址
    def _get_titles_urls_and_imgs(self, url: str):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        titles = soup.select('section.entry.entry-archive h2 a')
        imgs = soup.select('article img')

        self.titles = [title.text.strip() for title in titles]
        self.urls = [title['href'] for title in titles]
        self.img_urls = [img['src'] for img in imgs]
    
    # 新聞稿
    def get_news(self):
        url = 'https://towerofsaviors.com/category/新聞稿/'
        self._get_titles_urls_and_imgs(url)
        
    # 慶祝活動
    def get_announcement(self):
        url = 'https://towerofsaviors.com/category/公告/'
        self._get_titles_urls_and_imgs(url)

        for i in range(len(self.titles) - 1, -1, -1):
            if '慶祝活動' not in self.titles[i]:
                del self.titles[i]
                del self.urls[i]
                del self.img_urls[i]
    
    def __str__(self) -> str:
        return (
            f'標題: {self.titles[0]}\n'
            f'連結: {self.urls[0]}\n'
            f'圖片: {self.img_urls[0]}\n'
        )

if __name__ == '__main__':
    tos = TowerOfSaviors()
    # 新聞稿
    tos.get_news()
    print('\n新聞稿:')
    print(tos)

    # 慶祝活動
    tos = TowerOfSaviors()
    tos.get_announcement()
    print('\n慶祝活動:')
    print(tos)
