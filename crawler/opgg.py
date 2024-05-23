import requests
from bs4 import BeautifulSoup
import json
from crawler.crawler_classes import Crawler
# from crawler_classes import Crawler

class OPGG:
    def __init__(self, lol_id: str):
        self.lol_id = lol_id
        # self.winning_rate = None
    
    def get_r(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        }
        r = requests.get(url, headers=headers)
        return r
    
    
    # def get_winning_rate(self, game_type='單/雙排'):
    #     with open("data/opgg/game_type.json", "r", encoding="utf-8") as json_file:
    #         data = json.load(json_file)
    #     for type in data['game_type']:
    #         if type['game_translate'] == game_type:
    #             game_type_en = type['game_type']
    #             break
        
    #     url = f'https://lol-web-api.op.gg/api/v1.0/internal/bypass/summoners/tw/{self.lol_id}/most-champions/rank?game_type={game_type_en}'
    #     r = Crawler.get_r(url)
    #     data = r.json()
    #     if data['data']:
    #         win = data['data']['win']
    #         play = data['data']['play']
    #         self.winning_rate = f'{win / play * 100:.2f}%'
    #     else:
    #         self.winning_rate = f'沒有進行過{game_type}對戰'

class Summoner(OPGG):
    def __init__(self, lol_id: str):
        super().__init__(lol_id)

        # https://lol-web-api.op.gg/api/v1.0/internal/bypass/summoners/tw/kAUMc-mNpagwXioYpaRRWtJu9JYxYymfy2kICeyxNMlqciMmK6ES9qq-Sw?hl=zh_TW
        summoner_url = f'https://lol-web-api.op.gg/api/v1.0/internal/bypass/summoners/tw/{self.lol_id}?hl=zh_TW'
        r = Crawler.get_r(summoner_url)

        self.summoner_data = r.json()['data']

        # 遊戲名稱
        self.game_name = self.summoner_data['game_name']
    
    def __str__(self) -> str:
        return (
            f'遊戲名稱: {self.game_name}\n'
        )

class InGame(OPGG):
    def __init__(self, lol_id: str):
        super().__init__(lol_id)

        in_game_url = f'https://lol-web-api.op.gg/api/v1.0/internal/bypass/spectates/tw/{self.lol_id}?hl=zh_TW'
        r = Crawler.get_r(in_game_url)
        
        # 是否在遊戲中
        if r.status_code == 200:
            self.is_in_game = True
            self.in_game_data = r.json()['data']

            # 遊戲 id
            self.game_id = self.in_game_data['game_id']

            # 取得當前遊戲模式
            self.game_type = self.in_game_data['queue_info']['queue_translate']
        else:
            self.is_in_game = False
    
    def get_team_data(self):
        with open("crawler/test.json", "r", encoding="utf-8") as json_file:
            self.in_game_data = json.load(json_file)['data']

        participants = self.in_game_data['participants']
        teams = self.in_game_data['teams']

        new_in_game_data = {
            'participants': [
                {
                    'summoner': {
                        'summoner_id': p['summoner']['summoner_id'],
                        'game_name': p['summoner']['game_name'],
                        'level': p['summoner']['level'],
                        'previous_tier_info': {
                            'tier': p['summoner']['previous_seasons'][0]['tier_info']['tier'],
                            'division': p['summoner']['previous_seasons'][0]['tier_info']['division'],
                            'tier_image_url': p['summoner']['previous_seasons'][0]['tier_info']['tier_image_url']
                        } if p['summoner']['previous_seasons'] else {},
                        'tier_info': {
                            'tier': p['summoner']['league_stats'][0]['tier_info']['tier'],
                            'division': p['summoner']['league_stats'][0]['tier_info']['division'],
                            'lp': p['summoner']['league_stats'][0]['tier_info']['lp'],
                            'tier_image_url': p['summoner']['league_stats'][0]['tier_info']['tier_image_url'],
                            'win': p['summoner']['league_stats'][0]['win'],
                            'lose': p['summoner']['league_stats'][0]['lose']
                        } if p['summoner']['league_stats'] else {}
                    },
                    'team_key': p['team_key'],
                    'champion_id': p['champion_id'],
                    'position': p['position']
                } for p in participants
            ],
            'teams': [
                {
                    'key': team['key'],
                    'average_tier_info': {
                        'tier': team['average_tier_info']['tier'],
                        'division': team['average_tier_info']['division'],
                        'tier_image_url': team['average_tier_info']['tier_image_url']
                    }
                } for team in teams
            ]
        }

        sorted_new_game_data = sorted(new_in_game_data['participants'], key=lambda x: (x['team_key'] != 'BLUE', x['team_key'], ['TOP', 'JUNGLE', 'MID', 'ADC', 'SUPPORT'].index(x['position'])))
        self.team_data = sorted_new_game_data

        # with open('crawler/test_output.json', 'w', encoding='utf8') as jfile:
        #     json.dump(self.team_data, jfile, ensure_ascii=False, indent=4)



    def __str__(self) -> str:
        if self.is_in_game:
            return (
                f'是否在遊戲內:\t {self.is_in_game}\n'
                f'遊戲 id:\t {self.game_id}\n'
                f'遊戲模式:\t {self.game_type}\n'
            )
        else:
            return (
                f'是否在遊戲內: {self.is_in_game}\n'
            )

class GameData(OPGG):
    def __init__(self, lol_id: str, game_type: str = 'total', limit: int = 20):
        super().__init__(lol_id)

        self.game_type = game_type
        self.limit = limit

        # https://lol-web-api.op.gg/api/v1.0/internal/bypass/games/tw/summoners/kAUMc-mNpagwXioYpaRRWtJu9JYxYymfy2kICeyxNMlqciMmK6ES9qq-Sw?&limit=20&hl=zh_TW&game_type=total
        game_data_url = f'https://lol-web-api.op.gg/api/v1.0/internal/bypass/games/tw/summoners/{self.lol_id}?&limit={self.limit}&hl=zh_TW&game_type={self.game_type}'
        r = Crawler.get_r(game_data_url)

        self.game_data = r.json()['data']
        self.last_game_id = self.game_data[0]['id']
    
    def __str__(self) -> str:
        return (
            f'最後一場遊戲id: {self.last_game_id}\n'
        )


if __name__ == '__main__':
    # 測試時需改成
    # from crawler_classes import Crawler

    # 再吵就送
    # player_id = 'kAUMc-mNpagwXioYpaRRWtJu9JYxYymfy2kICeyxNMlqciMmK6ES9qq-Sw'
    # 中飛妮可
    player_id = '1nXTkNy9PF9RGpU4P_kFz-49_aze2BUmOXCtJDPOuPsw3_IZY9cRPA2Hlg'

    # 是否在遊戲中
    player_in_game = InGame(player_id)
    print(player_in_game)
    player_in_game.get_participants_data()

    # # 玩家資訊
    # player_summoner = Summoner(player_id)
    # print(player_summoner)

    # # 遊戲數據
    # player_game_data = GameData(player_id, limit=1)
    # print(player_game_data)
