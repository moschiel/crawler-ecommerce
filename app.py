#! /usr/bin/env python3
import utils as u
import constants as c
import lxml.html as parser
import requests
from time import sleep


def setTabUrls(startTab=0, count=0):
    print("SETANDO URLs DE CADA ABA")
    urls = []
    for index in range(count):
        char_tab = u.NumberToLetter(startTab + index)
        url = "https://www.americanas.com.br/mapa-do-site/lojista/f/letra-" + char_tab
        urls.append(url)
        if(c.PRINT_ABA_URL):
            print (url)
    u.endline()
    return urls

def getPagesPerTab(TabUrls):
    print("COLETANDO URL DE PAGINAS DE CADA ABA")
    pages_per_tab = []
    for url in TabUrls:
        #read last character
        char_tab = url[-1:] if url[-1:] != "0" else "#" 
        try:
            sleep(0.5) #delay pra evitar detecção de requests massivos
            #intercala entre a url da home e a url que queremos, para assim burlar a detecção de repetição de rotas
            requests.get("https://www.americanas.com.br", headers=c.HEADERS)
            page = requests.get(url, headers=c.HEADERS)
            if(page.status_code != 200):
                print("ERRO NA LEITURA DE PAGINAS DA ABA '" + char_tab + "', STATUS CODE: " + str(page.status_code))
                continue

            tree = parser.fromstring(page.content)
            page_urls = tree.xpath('//*[@id="summary-pane-'+ char_tab +'"]/div/div/div/div/ul/li/a/@href')
            page_urls = u.RemoveDuplicates(page_urls) 
            page_urls = u.RemoveIfContain(page_urls, "#")
            print("coletado " + str(len(page_urls)) + " urls de pagina da aba '" + char_tab + "'")  
            
            for i in range(len(page_urls)):
                if(("pagina" not in page_urls[i]) and ("letra" in page_urls[i])):
                    page_urls[i] += "/pagina-1"
                page_urls[i] = "https://www.americanas.com.br" + page_urls[i]
                if c.PRINT_PAGE_URL:
                    print(page_urls[i])
           
            pages_per_tab.append(page_urls)
        except:
            print("ERRO NA LEITURA DE PAGINAS DA ABA '" + char_tab + "'")
    u.endline() 
    return pages_per_tab

def getSellersPerTab(urlsPerPagePerTab):
    print ("COLETANDO URL DOS SELLERS DE CADA ABA")

    sellersUrls = []
    totalSellers = 0
    for pagesUrls in urlsPerPagePerTab:
        char_pos = pagesUrls[0].index('letra-') + len('letra-')
        char_tab = pagesUrls[0][char_pos] if pagesUrls[0][char_pos] != "0" else "#"
        sellersUrlsCollected = []
        StatudCodeFail = False
        for pageUrl in pagesUrls:
            try:
                sleep(0.5) #delay pra evitar detecção de requests massivos
                #intercala entre a url da home e a url que queremos, para assim burlar a detecção de repetição de rotas
                requests.get("https://www.americanas.com.br", headers=c.HEADERS)
                page = requests.get(pageUrl, headers=c.HEADERS)

                if(page.status_code != 200):
                    #print("ERRO NA LEITURA DOS SELLERS DA ABA '" + char_tab + "', PAGINA " + pageUrl[-1:] + ", STATUS CODE: " + str(page.status_code))
                    StatudCodeFail = True
                    continue
                tree = parser.fromstring(page.content)
                page_urls = tree.xpath('//*[@id="summary-pane-' + char_tab + '"]/div/ul/li/ul/li/h3/a/@href')
                sellersUrlsCollected += page_urls
            except:
                print("ERRO NA COLETA DE URLS DA PAGINA '" + pageUrl[-1:] + "'")
        #quando trocavamos de pagina no for acima, muitas urls vem repetido
        sellersUrlsCollected = u.RemoveDuplicates(sellersUrlsCollected) 
        #algumas urls falsas geralmente tem a substring '-teste'
        sellersUrlsCollected = u.RemoveIfContain(sellersUrlsCollected, '-teste') 
        if c.PRINT_SELLERS_URL:
            for url in sellersUrlsCollected:
                print(url)
        numCollected = len(sellersUrlsCollected)
        totalSellers += numCollected
        print("coletado " + str(numCollected) + " urls de sellers da aba '" + char_tab + "' - COMPLETE:" + str(not StatudCodeFail))
        
    u.endline()
    print("TOTAL DE URLS DE SELLERS: " + str(totalSellers))
    u.endline()



start_tab = 0
count = c.MAX_ABAS
tabUrls = setTabUrls(start_tab, count)
pagesPerTabUrls = getPagesPerTab(tabUrls)
getSellersPerTab(pagesPerTabUrls)
