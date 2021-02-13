MAX_LETTER = 27
PRINT_ABA_URL = True
PRINT_PAGE_URL = False
PRINT_SELLERS_URL = False
REQUEST_INTERVAL = 2 #seconds

HEADERS_AMERICANAS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36', 
    #"Upgrade-Insecure-Requests": "1",
    "dnt": "1",
    #"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    #accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", 
    "accept": "*/*",
    "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "accept-encoding": "gzip, deflate, br",
    "origin": "https://www.americanas.com.br",
    "referer": "https://www.americanas.com.br/",
    "sec-ch-ua": '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site"
}

HEADERS_RECLAMEAQUI = {
    'Accept' : 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'iosearch.reclameaqui.com.br',
    'Origin': 'https://www.reclameaqui.com.br',
    'Referer': 'https://www.reclameaqui.com.br/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36'
}
