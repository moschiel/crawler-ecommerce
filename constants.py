MAX_ABAS = 27
PRINT_ABA_URL = True
PRINT_PAGE_URL = False
PRINT_SELLERS_URL = False
REQUEST_INTERVAL = 2 #seconds

HEADERS = {
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
