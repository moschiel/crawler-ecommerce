#! /usr/bin/env python3
import utils as u
import constants as c
import lxml.html as parser
import requests
from time import sleep
import file_manager as f
import json

#seta a rota para visualizar os lojistas por aba/letra
#Ex: https://www.americanas.com.br/mapa-do-site/lojista/f/letra-a
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

#cada aba/letra, tem um numero de paginas, coletamos cada url de pagina de cada aba/letra
#Ex: 
# https://www.americanas.com.br/mapa-do-site/lojista/f/letra-a/pagina-1
# https://www.americanas.com.br/mapa-do-site/lojista/f/letra-a/pagina-2 
# ...
def getPagesPerTabUrls(TabUrls):
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

#coleta a url individual de cada seller, por aba/letra
#Ex: https://www.americanas.com.br/lojista/3n-s-lasers
def getSellersPerTabUrls(urlsPerPagePerTab):
    print ("COLETANDO URL DOS SELLERS DE CADA ABA")
    sellersUrls = []
    totalSellers = 0
    for pagesUrls in urlsPerPagePerTab:
        char_tab = pagesUrls[0][0] if pagesUrls[0][0] != "0" else "#"
        sellersCollectedJson = f.read_file("url_sellers", "url_sellers_tab_" + char_tab + ".json")

        if(sellersCollectedJson != False):
            sellersCollectedJson = json.loads(sellersCollectedJson)
            print("carregado " + str(len(sellersCollectedJson)) + " urls de sellers da aba '" + char_tab + "'")
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
            #converte para um formato json mais legível
            sellersCollectedJson = []
            for url in sellersUrlsCollected:
                sellersCollectedJson.append({
                    "ecomm_info": {
                        "url": "https://www.americanas.com.br" + url
                    }
                })

            f.save_file("url_sellers", "url_sellers_tab_" + char_tab + ".json", json.dumps(sellersCollectedJson))
            print("salvo " + str(len(sellersCollectedJson)) + " urls de sellers da aba '" + char_tab + "' - COMPLETE:" + str(not StatudCodeFail))
        
        totalSellers += len(sellersCollectedJson)
        sellersUrls.append(sellersCollectedJson)
    u.endline()
    print("TOTAL DE URLS DE SELLERS: " + str(totalSellers))
    u.endline()
    return sellersUrls


class Seller:
    name = ""
    rating = 0
    votes = 0
    products = 0
    categories = []

def getSellersData(sellersPerTab):
    print ("COLETANDO DADOS DOS SELLERS DE CADA ABA")
    pos_char = len("https://www.americanas.com.br/lojista/")
    
    for row in range(len(sellersPerTab)): #each row is a tab
        char_tab = sellersPerTab[row][0]['ecomm_info']['url'][pos_char]
        if (char_tab.isnumeric()):
            char_tab = "#"
        print ("COLETANDO DADOS DOS SELLERS DA ABA '"+ char_tab+ "'")

        for col in range(len(sellersPerTab[row])):  #each colum is a seller within this tab
            url = sellersPerTab[row][col]['ecomm_info']['url']
            #url = "https://www.americanas.com.br/lojista/webcontinental"
            
            if(True):
            #try:
                while (True): #emula Do-While - enquanto status==202, repita
                    sleep(c.REQUEST_INTERVAL) #delay pra evitar detecção de requests massivos
                    page = requests.get(url, headers=c.HEADERS)
                    if(page.status_code != 202):
                        break
                    else:
                        print("Re-try Status: " + str(page.status_code))
    
                if(page.status_code != 200):
                    StatudCodeFail = True
                    #continue
                    print("ERRO NA LEITURA DOS SELLER DA ABA '" + char_tab + "': " + url + ", STATUS CODE: " + str(page.status_code))
                    return
                
                seller = Seller()
                tree = parser.fromstring(page.content)
                seller.name = tree.xpath('//*[@id="main-top"]/div[1]/div/ol/li[2]/a/@name')[0]
                seller.cnpj = tree.xpath('//*[@id="main-top"]/div[1]/div/ol/li[2]/a/@id')[0]
                
                #alguns logistas podem não ter rankings
                try:
                    seller.rating = tree.xpath('//*[@id="main-top"]/div[4]/div/div/div/div/div/div/div[2]/div[1]/text()')[0]  
                    seller.rating = float(seller.rating)
                    seller.votes = tree.xpath('//*[@id="main-top"]/div[4]/div/div/div/div/div/div/div[2]/div[2]/text()')[0]
                    seller.votes = seller.votes.replace("avaliações", "").strip()
                    seller.votes = seller.votes.replace(".", "")
                    seller.votes = int(seller.votes)
                except:
                    seller.rating = "--"
                    seller.votes = "--"

                #alguns logistas não tem produtos
                try:
                    seller.products = tree.xpath('//*[@id="sort-bar"]/div/aside/div/div[1]/span/text()')[0]
                    seller.products = seller.products.replace("produtos", "").strip()
                    seller.products = seller.products.replace(".", "")
                    seller.products = int(seller.products)
                except:
                    seller.products = "--"

                #print(seller.name, seller.cnpj, seller.rating, seller.votes, seller.products)

                categoriesName = tree.xpath('//*[@id="collapse-categorias"]/ul/li/a/span/text()')
                categoriesCount = tree.xpath('//*[@id="collapse-categorias"]/ul/li/a/@data-results-count') 
                #print(categoriesName)
                #print(categoriesCount)
                
                #monta json das categorias
                seller.categories = [] #bugfix, limpando a cada iteracao, em teoria nao precisava pois seller = Seller() tinha que vir limpo 
                for i in range(len(categoriesName)):
                    seller.categories.append({
                        "name": categoriesName[i],
                        "count": int(categoriesCount[i])
                    })

                #insere dados do seller no json
                sellersPerTab[row][col]['ecomm_info'].update({
                    "name": seller.name,
                    "cnpj": seller.cnpj,
                    "rating": seller.rating,
                    "votes": seller.votes,
                    "products": seller.products,
                    "categories": seller.categories
                })
                
                print(str(col) + ": " + seller.name)
                if(col == 3):
                    break

                #break
            #except:
            #    print("ERRO NA LEITURA DO SELLER NA ABA '"+ char_tab+ "': " + url)
            #    return
            #return   

        f.save_file("data_sellers", "data_sellers_tab_" + char_tab + ".json", json.dumps(sellersPerTab[row]))  

