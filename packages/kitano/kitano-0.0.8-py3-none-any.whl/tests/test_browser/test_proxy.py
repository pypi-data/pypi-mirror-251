from kitano.browser import metamorproxies as proxies

def test_proxies():
    #proxies
    # print(proxies.proxy_caliwyr(),'\n')
    # print(proxies.proxy_hanway(),'\n')
    # print(proxies.proxy_shift(),'\n')
    
    #assert proxies.proxy_caliwyr(), 'proxies caliwyr is not ok'
    assert proxies.proxy_shift(), 'proxies shift is not ok'
    assert proxies.proxy_hanway(), 'proxies hanway is not ok'
    
    
    #socks
    # print(proxies.socks_hook(),'\n')
    # print(proxies.socks_shift(),'\n')
    # print(proxies.socks_murong(),'\n')
    
    assert proxies.socks_hook(), 'socks hook is not ok'
  #  assert proxies.socks_shift(), 'socks shift is not ok'
    assert proxies.socks_murong(), 'socks murong is not ok'
    
    



