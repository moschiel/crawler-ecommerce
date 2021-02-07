#! /usr/bin/env python3
import utils as u
import constants as c
import lxml.html as parser
import requests
from time import sleep
import file_manager as f
import json

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
            page_urls = f.read_file("url_pages_tab", "url_pages_tab_" + char_tab + ".json")
            if(page_urls != False):
                page_urls = json.loads(page_urls)
                print("carregado " + str(len(page_urls)) + " urls de pagina da aba '" + char_tab + "'") 
            else:
                sleep(c.REQUEST_INTERVAL) #delay pra evitar detecção de requests massivos, o que causaria error 403
                page = requests.get(url, headers=c.HEADERS)
                if(page.status_code != 200):
                    print("ERRO NA LEITURA DE PAGINAS DA ABA '" + char_tab + "', STATUS CODE: " + str(page.status_code))
                    continue

                tree = parser.fromstring(page.content)
                page_urls = tree.xpath('//*[@id="summary-pane-'+ char_tab +'"]/div/div/div/div/ul/li/a/@href')
                page_urls = u.RemoveDuplicates(page_urls) 
                page_urls = u.RemoveIfContain(page_urls, "#")  
            
                for i in range(len(page_urls)):
                    if(("pagina" not in page_urls[i]) and ("letra" in page_urls[i])):
                        page_urls[i] += "/pagina-1"
                    page_urls[i] = page_urls[i][30:] # armazena apenas o conteudo depois da string 'letra-'
                    if c.PRINT_PAGE_URL:
                        print(page_urls[i])
                f.save_file("url_pages_tab", "url_pages_tab_" + char_tab + ".json", json.dumps(page_urls))
                print("salvo " + str(len(page_urls)) + " urls de pagina da aba '" + char_tab + "'")

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
        char_tab = pagesUrls[0][0] if pagesUrls[0][0] != "0" else "#"
        sellersUrlsCollected = f.read_file("url_sellers", "url_sellers_tab_" + char_tab + ".json")

        if(sellersUrlsCollected != False):
            sellersUrlsCollected = json.loads(sellersUrlsCollected)
            print("carregado " + str(len(sellersUrlsCollected)) + " urls de sellers da aba '" + char_tab + "'")
        else:
            sellersUrlsCollected = []
            StatudCodeFail = False
            for pageUrl in pagesUrls:
                try:
                    sleep(c.REQUEST_INTERVAL) #delay pra evitar detecção de requests massivos, o que causaria error 403
                    page = requests.get("https://www.americanas.com.br/mapa-do-site/lojista/f/letra-" + pageUrl, headers=c.HEADERS)

                    if(page.status_code != 200):
                        StatudCodeFail = True
                        #continue
                        print("ERRO NA LEITURA DOS SELLERS DA ABA '" + char_tab + "', PAGINA " + pageUrl[-1:] + ", STATUS CODE: " + str(page.status_code))
                        return
                    tree = parser.fromstring(page.content)
                    page_urls = tree.xpath('//*[@id="summary-pane-' + char_tab + '"]/div/ul/li/ul/li/h3/a/@href')
                    sellersUrlsCollected += page_urls
                except:
                    print("ERRO NA COLETA DE URLS DA PAGINA '" + pageUrl[-1:] + "'")
            #quando trocavamos de pagina no for acima, muitas urls vem repetido
            sellersUrlsCollected = u.RemoveDuplicates(sellersUrlsCollected) 
            #algumas urls falsas geralmente tem a substring '-teste'
            sellersUrlsCollected = u.RemoveIfContain(sellersUrlsCollected, '-teste') 
            
            for i in range(len(sellersUrlsCollected)):
                sellersUrlsCollected[i] = sellersUrlsCollected[i][9:] # armazena apenas o conteudo depois da string '/lojista/'
                if c.PRINT_SELLERS_URL:
                    print(sellersUrlsCollected[i])

            f.save_file("url_sellers", "url_sellers_tab_" + char_tab + ".json", json.dumps(sellersUrlsCollected))
            print("salvo " + str(len(sellersUrlsCollected)) + " urls de sellers da aba '" + char_tab + "' - COMPLETE:" + str(not StatudCodeFail))
        
        totalSellers += len(sellersUrlsCollected)
        sellersUrls.append(sellersUrlsCollected)
    u.endline()
    print("TOTAL DE URLS DE SELLERS: " + str(totalSellers))
    u.endline()
    return sellersUrls
