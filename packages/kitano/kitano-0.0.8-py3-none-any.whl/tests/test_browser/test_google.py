from bs4 import BeautifulSoup
from requests import get
from time import sleep

from kitano.browser import metamorproxies as proxies
#from getpdf.google.user_agents import get_useragent


headers = {'user-agent':'Mozilla/5.0 (Linux; U; Android 4.4.2; zh-cn; GT-I9500 Build/KOT49H) AppleWebKit/537.36(KHTML, like Gecko)Version/4.0 MQQBrowser/5.0 QQ-URL-Manager Mobile Safari/537.36',
            'connection': 'keep-alive', 'upgrade-insecure-requests': '1', 
#            'user-agent': 'Mozilla/5.0 (Linux; Android 12; SM-A225M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'pt-BR,pt-PT;q=0.9,pt;q=0.8,en-US;q=0.7,en;q=0.6'}

def _req(term, results, lang, start, proxies):
    resp = get(
        url="https://www.google.com/search",
        headers=headers,
        params=dict(
            q=term,
            num=results + 2,  # Prevents multiple requests
            hl=lang,
            start=start,
        ),
        proxies=proxies,
    )
    resp.raise_for_status()
    return resp


class SearchResult:
    def __init__(self, url, title, description):
        self.url = url
        self.title = title
        self.description = description

    def __repr__(self):
        return f"SearchResult(url={self.url}, title={self.title}, description={self.description})"


def test_search(term, num_results=10, lang="en", proxy=None, advanced=False, sleep_interval=0):
    escaped_term = term.replace(" ", "+")

    # Proxy
    # proxies = None
    # if proxy:
    #     if proxy.startswith("https"):
    #         proxies = {"https": proxy}
    #     else:
    #         proxies = {"http": proxy}
    prox = proxies.api_proxy()[0]
    proxi = f'https://{prox["ip"]}:{prox["port"]}'
    proxies = {'https':proxi}
    # Fetch
    start = 0
    while start < num_results:
        # Send request
        try:
            resp = _req(escaped_term, num_results - start, lang, start, proxies)

            # Parse
            soup = BeautifulSoup(resp.text, "html.parser")
            result_block = soup.find_all("div", attrs={"class": "g"})
            for result in result_block:
                # Find link, title, description
                link = result.find("a", href=True)
                title = result.find("h3")
                description_box = result.find("div", {"style": "-webkit-line-clamp:2"})
                if description_box:
                    description = description_box.find("span")
                    if link and title and description:
                        start += 1
                        if advanced:
                            yield SearchResult(link["href"], title.text, description.text)
                        else:
                            yield link["href"]
            sleep(sleep_interval)
        except:
            print('oh shits. lats go again')
            test_search(term=term, num_results=num_results, lang=lang, proxy=proxy, advanced=advanced, sleep_interval=sleep_interval)

