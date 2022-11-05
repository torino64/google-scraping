from bs4 import BeautifulSoup
import requests
import json
import csv

class GoogleScraper:
    base_url='https://www.google.com/search'
    numpage=0

    pagination_params={
        'q': '',
        'rlz': '1C1UEAD_frUS964US964',
        'sxsrf': 'AOaemvLhHDtESN4pWCLKASC14EaK-9-2dg:1634914772971',
        'ei': '1NFyYYnTOsyelwSis6-QBA',
        'start': '',
        'sa': 'N',
        'ved': '2ahUKEwiJjZ-SpN7zAhVMz4UKHaLZC0IQ8tMDegQIARA7',
        'biw': '585',
        'bih': '568',
        'dpr': '1.1'
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'private, max-age=0',
        'cookie': 'CONSENT=PENDING+614; HSID=A8JBjjzJua2iel49w; SSID=ATIv95Je4wKXHI9HQ; APISID=iOaQHR2ddFIVpgh4/AGBD8sRF0483q1w3G; SAPISID=50jfMFm5fa8XWYZh/A4C2CF0Q8FnpKpsZH; __Secure-1PAPISID=50jfMFm5fa8XWYZh/A4C2CF0Q8FnpKpsZH; __Secure-3PAPISID=50jfMFm5fa8XWYZh/A4C2CF0Q8FnpKpsZH; SEARCH_SAMESITE=CgQI0ZMB; SID=CAh51VK0d5cs2w9aHJeHoeRB3UwqDuNuNJqrDz_fglBSl7rgpKvCC64xTpoy0pt6IGE3rA.; __Secure-1PSID=CAh51VK0d5cs2w9aHJeHoeRB3UwqDuNuNJqrDz_fglBSl7rgq-yjsSBi9F6hoEWVP4-JqA.; __Secure-3PSID=CAh51VK0d5cs2w9aHJeHoeRB3UwqDuNuNJqrDz_fglBSl7rgkH0w3rv7rLsFnvgYHeOZaA.; OGPC=19025836-2:19026101-2:; __Secure-1PSIDCC=AJi4QfGuvmKrHisTs00G7TrVH-BxBmHqYPvLslTFobGfVEfzA34T8aqAtcVZtwJ639jAzyWf6Q; NID=511=Mmq39xTvY-2NgipA2g1gK0YuTaB-AzOQ00ny0Ek-9w_qKoQ9wsvjc2kNfEjLxCTknD0q1lqPDg-k1K6RUfFf9n28nMN5ur20x3xiTt-THRWFndWS2oXMpoESpoO41A0q5_PpZ9wiWTkGkwnzaqLXgFFOdlN-0waWosO9g8XHiD6FWXaOBXZ2Wtc2648duexVAdbnaXoHzVrNkNZpsIuHSdtsqKuDDmXlw5GyZjQnviUX4zaaEWLeYeuxYHYuJM5ntYNB_ZbhOX-h; 1P_JAR=2021-10-22-15; SIDCC=AJi4QfEvOUty0t2BLbEu0JA-7yxQK1Er4fjVBtvAqp4b7OK7AyVb_g-EIzxsYtC2jR7yx6WsxQ; __Secure-3PSIDCC=AJi4QfFXZqJOmu5sVPRVstDs1C9ILtFT1D_NxbyteUOsd8lu7f95CfdzyDsPhjh4D3_IVs6ItA',
        'pragma':'no-cache',
        'referer': 'https://www.google.com/',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
    }
    
    params = {
        'q': '',
        'rlz': '1C1UEAD_frUS964US964',
        'biw': '585',
        'bih': '568',
        'sxsrf': 'AOaemvJGO8hPAf5HR6CkFitW71SQMPa2Lw:1634914845671',
        'ei': 'HdJyYa-sKNKaa_2Ll-AE',
        'ved': '0ahUKEwjvrvS0pN7zAhVSzRoKHf3FBUw4ChDh1QMIDg',
        'uact': '5',
        'oq': '',
        'gs_lcp': 'Cgdnd3Mtd2l6EAMyBwgjELADECcyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAELADEENKBAhBGABQAFgAYKPaWmgBcAJ4AIABAIgBAJIBAJgBAMgBCsABAQ',
        'sclient': 'gws-wiz'
    }
    
    def fetch(self, query):
        if self.numpage==0:
            self.params['q']=query
            self.params['oq']=query
            response = requests.get(self.base_url, params=self.params, headers=self.headers)
        else:
            self.pagination_params['q']=query
            self.pagination_params['start']=str(self.numpage)
            response = requests.get(self.base_url, params=self.pagination_params, headers=self.headers)
        if response.status_code == 200:
            return response.text
        else:
            return 0

    def parse(self, html):
        content = BeautifulSoup(html, 'lxml')
        link= [link.next_element['href'] for link in content.findAll('div', 'yuRUbf')]
        return link
    
    def run(self, key,max=1):
        urls=[]
        while self.numpage <= max:
            data=self.fetch(key)
            alldata=self.parse(data)
            urls.append(alldata)
            self.numpage+=10
        return urls
            





