import requests as rq


#print(proxy_list_caliwyr)
def proxy_caliwyr():
    proxy_list_caliwyr = rq.get('https://raw.githubusercontent.com/caliwyr/free-proxy-list/main/proxy-list/data-with-geolocation.json')
    if proxy_list_caliwyr.status_code == 200:
        proxy = [{"https":f"{proxi['ip']}:{proxi['port']}"} for proxi in proxy_list_caliwyr.json()]
        return proxy
    else:
        return False



def proxy_shift():
    proxy_shift_http = rq.get('https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt')
    proxy_shift_https = rq.get('https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt')
    res = {}
    if (proxy_shift_http.status_code == 200) and (proxy_shift_https.status_code == 200):
        # print(proxy_shift_http.text.split('\n'))
        res['http'] = [{'ip':proxi.split(':')[0],'port':proxi.split(':')[1]} for proxi in proxy_shift_http.text.split('\n')[:-1]]
        res['https'] = [{'ip':proxi.split(':')[0],'port':proxi.split(':')[1]} for proxi in proxy_shift_https.text.split('\n')[:-1]]
        return res
    else:
        return False



def proxy_hanway():
    proxy_hanway_http = rq.get('https://raw.githubusercontent.com/hanwayTech/free-proxy-list/main/http.txt')
    proxy_hanway_https = rq.get('https://raw.githubusercontent.com/hanwayTech/free-proxy-list/main/https.txt')
    res = {}
    if (proxy_hanway_http.status_code == 200) and (proxy_hanway_https.status_code == 200):
        res['http'] = [{'ip':proxi.split(':')[0],'port':proxi.split(':')[1]} for proxi in proxy_hanway_http.text.split('\n')[:-1]]
        res['https'] = [{'ip':proxi.split(':')[0],'port':proxi.split(':')[1]} for proxi in proxy_hanway_https.text.split('\n')[:-1]]
        return res
    else:
        return False




def socks_shift():
    socks5_shift_req = rq.get('https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt')
    socks4_shift_req = rq.get('https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt')
    res = {}
    if socks4_shift_req.status_code ==200 and socks5_shift_req.status_code==200:
        res['socks4'] = [{'ip':socks4.split(':')[0],'port':socks4.split(':')[1]} for socks4 in socks4_shift_req.text.split('\n')[:-1]]
        res['socks5'] = [{'ip':socks5.split(':')[0],'port':socks5.split(':')[1]} for socks5 in socks5_shift_req.text.split('\n')[:-1]]
        return res
    else:
        return False


def socks_hook():
    socks5_hook_req = rq.get('https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt')
    res = {}
    if socks5_hook_req.status_code==200:
        res['socks5'] = [{'ip':socks5.split(':')[0],'port':socks5.split(':')[1]} for socks5 in socks5_hook_req.text.split('\n')[:-1]]
        return res
    else:
        return False

def socks_murong():
    socks5_murong_req = rq.get('https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks5.txt')
    socks4_murong_req = rq.get('https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks4.txt')
    res = {}
    if socks5_murong_req.status_code==200 and socks4_murong_req.status_code==200:
        res['socks5'] = [{'ip':socks5.split(':')[0],'port':socks5.split(':')[1]} for socks5 in socks5_murong_req.text.split('\n')[:-1]]
        res['socks4'] = [{'ip':socks4.split(':')[0],'port':socks4.split(':')[1]} for socks4 in socks4_murong_req.text.split('\n')[:-1]]
        return res
    else:
        return False


def api_proxy():
    proxi = rq.get('https://www.proxyscan.io/api/proxy?ping=100')
    if proxi.status_code==200:
        if proxi.json()[0]['Location']['status']=='success':
            return proxi.json()
        else:
            return api_proxy()
    else:
        return False