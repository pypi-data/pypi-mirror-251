
import json
from requests.utils import cookiejar_from_dict
import requests as rq
import mechanicalsoup as mec
from requests_html import HTMLSession
asession = HTMLSession()
rq = asession
rq = mec.StatefulBrowser()
from kitano.browser import metamorproxies as proxies_
import random
from kitano.browser.heads import get_useragent

headers_main = {'user-agent':'Mozilla/5.0 (Linux; U; Android 4.4.2; zh-cn; GT-I9500 Build/KOT49H) AppleWebKit/537.36(KHTML, like Gecko)Version/4.0 MQQBrowser/5.0 QQ-URL-Manager Mobile Safari/537.36',
            'connection': 'keep-alive', 'upgrade-insecure-requests': '1', 
#            'user-agent': 'Mozilla/5.0 (Linux; Android 12; SM-A225M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'pt-BR,pt-PT;q=0.9,pt;q=0.8,en-US;q=0.7,en;q=0.6'}



def sniper_get(url:str,proxy:dict=None,headers:dict=None):
    headers_ = headers if headers else headers_main
    proxies=None
    res = rq.get(url,headers=headers_,proxies=proxies)
    #print(dir(res))
    print(res.status_code)
    if res.status_code==200:
        return res

    elif res.status_code==429:
        if proxy:
            if proxy.get('http',False):
                https = f'https://{proxy["https"]["ip"]}:{proxy["https"]["port"]}'
                http = f'https://{proxy["http"]["ip"]}:{proxy["http"]["port"]}'
                proxies={'https':https,'http':http}

                res = rq.get(url,headers=headers_,proxies=proxies)
                if res.status_code==200:
                    return res
                elif res.status_code==429:
                    print('oh shit, lats go again')
                    return sniper_get(url=url,proxy=proxy,headers=headers)

            else:

                https = f'{proxy["ip"]}:{proxy["port"]}'
                proxies={'https':https}

                res = rq.get(url,headers=headers_,proxies=proxies)
                if res.status_code==200:
                    return res
                elif res.status_code==429:
                    print('oh shit, lats go again')
                    return sniper_get(url=url,proxy=proxy,headers=headers)

        else:
            proxi=random.choice(proxies_.proxy_shift()['https'])
            https = f'{proxi["ip"]}:{proxi["port"]}'
            proxies={'https':https}
            print(proxies)
            rq.session.proxies.update(proxies)
            
            #headers = requests.utils.default_headers()
            rq.session.headers.update(headers_main)


            res = rq.get(url)
            print(res.status_code)
            if res.status_code==200:
                return res
            elif res.status_code==429:
                print('oh shit, lats go again')
                return sniper_get(url=url,proxy=proxy,headers=headers)

# def save_cookies(browser:br,path_cookies:str) -> str:
#     cookies = browser.session.cookies.get_dict()
#     cookies_json = json.dumps(cookies)
#     with open(path_cookies,'w') as file_cookies:
#         file_cookies.write(cookies_json)


# def load_cookies(browser:br,path_cookies:str) -> str:
#     with open(path_cookies,'r') as file_cookies:
#         cookies_json = file_cookies.read()
#         cookies_dict = json.loads(cookies_json)
#     browser.session.cookies = cookiejar_from_dict(cookie_dict=cookies_dict)
#     return browser