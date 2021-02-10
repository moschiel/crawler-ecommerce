#! /usr/bin/env python3
import utils as u
import constants as c
import lxml.html as parser
import requests
from time import sleep
import file_manager as f
import json

#coleta a url individual de cada seller, por letra
#Ex: https://www.americanas.com.br/lojista/3n-s-lasers
def getSellersByLetterUrls(letter):
    letter = u.NumberToLetter(letter)
    print ("COLETANDO URL DOS SELLERS DA LETRA " + letter)
    pageNumber = 0

    #verifica se existe arquivo, e continua coleta de onde parou
    sellersCollectedJson = f.read_file("url_sellers", "url_sellers_letter_" + letter + ".json")
    if(sellersCollectedJson != False):
        sellersCollectedJson = json.loads(sellersCollectedJson)
        print("carregado " + str(len(sellersCollectedJson)) + " urls de sellers da letra " + letter)
        print("continuando coleta ...")
        pageNumber = len(sellersCollectedJson)
    else:
        sellersCollectedJson = []

    sellersUrlsCollected = []
    countControl = 0
    while(True):  
        pageNumber = pageNumber + 1    
        print("page number: " + str(pageNumber))    
        try:
            while (True): #emula Do-While - enquanto status==202, repita
                sleep(c.REQUEST_INTERVAL) #delay pra evitar detecção de requests massivos
                ch = letter if letter != "#" else "0"
                pageNumberUrl = "https://www.americanas.com.br/mapa-do-site/lojista/f/letra-" + ch + "/pagina-" + str(pageNumber)
                page = requests.get(pageNumberUrl, headers=c.HEADERS)
                if(page.status_code != 202):
                    break
                else:
                    print("Re-try Status: " + str(page.status_code))
            
            if(page.status_code != 200):
                print("ERRO NA LEITURA DOS SELLERS DA LETRA '" + letter + "', PAGINA " + str(pageNumber) + ", STATUS CODE: " + str(page.status_code))
                return

            tree = parser.fromstring(page.content)
            page_urls = tree.xpath('//*[@id="summary-pane-' + letter + '"]/div/ul/li/ul/li/h3/a/@href')
            
            if(len(page_urls) > 0):
                sellersUrlsCollected += page_urls
            
            # a cada X paginas , ou se acabar as paginas, salvamos o arquivo
            countControl = countControl + 1
            if(countControl >= 10 or len(page_urls) == 0):
                print("salvando...")
                countControl = 0
                #quando trocavamos de pagina , muitas urls vem repetido
                sellersUrlsCollected = u.RemoveDuplicates(sellersUrlsCollected) 
                #algumas urls falsas geralmente tem a substring '-teste'
                sellersUrlsCollected = u.RemoveIfContain(sellersUrlsCollected, '-teste') 
                #converte para um formato json mais legível
                for url in sellersUrlsCollected:
                    sellersCollectedJson.append({
                        "ecomm_info": {
                            "url": "https://www.americanas.com.br" + url
                        }
                    })
                sellersUrlsCollected = []
                f.save_file("url_sellers", "url_sellers_letter_" + letter + ".json", json.dumps(sellersCollectedJson))

            if(len(page_urls) == 0):
                print("CONCLUIDO COLETA DE URLS DOS SELLERS DA LETRA " + letter)
                print("salvo " + str(len(sellersCollectedJson)) + " urls de sellers da letra " + letter)
                u.endline()
                break
        except:
            print("ERRO NA COLETA DE URLS DA LETRA " + letter + ", PAGINA " + str(pageNumber))

    return sellersCollectedJson


class Seller:
    name = ""
    rating = 0
    votes = 0
    products = 0
    categories = []

def getSellersData(sellersPerLetter):
    print ("COLETANDO DADOS DOS SELLERS DE CADA LETRA")
    pos_char = len("https://www.americanas.com.br/lojista/")
    
    for row in range(len(sellersPerLetter)): #each row is a letter
        letter = sellersPerLetter[row][0]['ecomm_info']['url'][pos_char]
        if (letter.isnumeric()):
            letter = "#"
        print ("COLETANDO DADOS DOS SELLERS DA LETRA '"+ letter+ "'")

        for col in range(len(sellersPerLetter[row])):  #each colum is a seller within this letter
            url = sellersPerLetter[row][col]['ecomm_info']['url']
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
                    print("ERRO NA LEITURA DOS SELLER DA LETRA '" + letter + "': " + url + ", STATUS CODE: " + str(page.status_code))
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
                sellersPerLetter[row][col]['ecomm_info'].update({
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
            #    print("ERRO NA LEITURA DO SELLER NA LETRA '"+ letter+ "': " + url)
            #    return
            #return   

        f.save_file("data_sellers", "data_sellers_letter_" + letter + ".json", json.dumps(sellersPerLetter[row]))  

