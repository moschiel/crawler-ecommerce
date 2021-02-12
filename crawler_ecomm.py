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

    #verifica se existe arquivo, e continua coleta de onde parou
    sellersJSON = f.read_file("url_sellers", "url_sellers_letter_" + letter + ".json")
    pageNumber = f.read_file("url_sellers", "url_sellers_letter_" + letter + "_last.txt")
    if(sellersJSON != False and pageNumber != False):
        sellersJSON = json.loads(sellersJSON)
        print("carregado " + str(len(sellersJSON)) + " urls de sellers da letra " + letter)
        pageNumber = int(pageNumber)
    else:
        sellersJSON = []
        pageNumber = 0

    sellersUrls = []
    saveControl = 0
    ch = letter if letter != "#" else "0"
    firstLoop = True
    while(True):  
        pageNumber = pageNumber + 1      
        try:
            while (True): #emula Do-While - enquanto status==202, repita
                sleep(c.REQUEST_INTERVAL) #delay pra evitar detecção de requests massivos
                pageNumberUrl = "https://www.americanas.com.br/mapa-do-site/lojista/f/letra-" + ch + "/pagina-" + str(pageNumber)
                page = requests.get(pageNumberUrl, headers=c.HEADERS)
                if(page.status_code != 202):
                    break
                else:
                    print("Re-try Status: " + str(page.status_code))
            
            if(page.status_code != 200):
                print("ERRO NA LEITURA DOS SELLERS DA LETRA '" + letter + "', PAGINA " + str(pageNumber) + ", STATUS CODE: " + str(page.status_code))
                return False

            tree = parser.fromstring(page.content)
            page_urls = tree.xpath('//*[@id="summary-pane-' + letter + '"]/div/ul/li/ul/li/h3/a/@href')
            
            if(firstLoop and len(page_urls) == 0): #if (firstLoop and (there is no more pages))
                u.endline()
                return sellersJSON #arquivo json carregado dessa letra ja estava concluida
            elif(len(page_urls) > 0):
                sellersUrls += page_urls    

            if(firstLoop):
                firstLoop = False
                if(pageNumber > 1):
                    print("continuando coleta apartir da pagina " + str(pageNumber))
            
            if(len(page_urls) == 0): #concluido a coleta
                u.endline() 
                break
            print("page number: " + str(pageNumber))

            # a cada X paginas , salvamos o arquivo
            saveControl = saveControl + 1
            if(saveControl >= 10):
                print("salvando...")
                saveControl = 0
                #quando trocavamos de pagina , muitas urls vem repetido
                sellersUrls = u.RemoveDuplicates(sellersUrls) 
                #algumas urls falsas geralmente tem a substring '-teste'
                sellersUrls = u.RemoveIfContain(sellersUrls, '-teste') 
                #converte para um formato json mais legível
                for url in sellersUrls:
                    sellersJSON.append({
                        "ecomm_info": {
                            "url": "https://www.americanas.com.br" + url
                        }
                    })
                sellersUrls = []
                f.save_file("url_sellers", "url_sellers_letter_" + letter + ".json", json.dumps(sellersJSON))
                f.save_file("url_sellers", "url_sellers_letter_" + letter + "_last.txt", str(pageNumber))
        except:
            print("ERRO NA COLETA DE URLS DA LETRA " + letter + ", PAGINA " + str(pageNumber))

    #antes de rotornar, percorre todo o Json pra remover duplicatas caso exista
    sellersJSON = u.RemoveDuplicates(sellersJSON) 
    f.save_file("url_sellers", "url_sellers_letter_" + letter + ".json", json.dumps(sellersJSON))
    f.save_file("url_sellers", "url_sellers_letter_" + letter + "_last.txt", str(pageNumber))  
    print("salvo " + str(len(sellersJSON)) + " urls de sellers da letra " + letter)
    u.endline() 
    return sellersJSON


class Seller:
    name = ""
    rating = 0
    votes = 0
    products = 0
    categories = []

def getSellersData(letter):
    letter = u.NumberToLetter(letter)
    print ("COLETANDO DADOS DOS SELLERS DA LETRA " + letter)

    #verifica se existe arquivo
    sellersJSON = f.read_file("data_sellers", "data_sellers_letter_" + letter + ".json")
    if(sellersJSON != False ):
        sellersJSON = json.loads(sellersJSON)
    else: #se nao existe, carrega arquivo de URLs da etapa anterior
        sellersJSON = f.read_file("url_sellers", "url_sellers_letter_" + letter + ".json")
        if sellersJSON != False:
            sellersJSON = json.loads(sellersJSON)
        else:
            print("Nenhum arquivo de URLs encontrado")
            return

    saveControl = 0
    for idx in range(len(sellersJSON)): 
        if("cnpj" in sellersJSON[idx]["ecomm_info"]):    
            # pula sellers ja coletados 
            # print(str(idx) + "(skipped)")
            continue
        
        url = sellersJSON[idx]['ecomm_info']['url']
        
        try:
            while (True): #emula Do-While - enquanto status==202, repita
                sleep(c.REQUEST_INTERVAL) #delay pra evitar detecção de requests massivos
                page = requests.get(url, headers=c.HEADERS)
                if(page.status_code != 202):
                    break
                else:
                    print("Re-try Status: " + str(page.status_code))

            if(page.status_code != 200):
                print("ERRO NA LEITURA DOS SELLER DA LETRA " + letter + " , " + url + " , STATUS CODE: " + str(page.status_code))
                return
            
            seller = Seller()
            tree = parser.fromstring(page.content)
            seller.name = tree.xpath('//*[@id="main-top"]/div[1]/div/ol/li[2]/a/@name')[0]
            seller.cnpj = tree.xpath('//*[@id="main-top"]/div[1]/div/ol/li[2]/a/@id')[0]
            
            #usado TRY pois alguns logistas podem não ter rankings
            try:
                seller.rating = tree.xpath('//*[@id="main-top"]/div[4]/div/div/div/div/div/div/div[2]/div[1]/text()')[0]  
                seller.rating = float(seller.rating)
                seller.votes = tree.xpath('//*[@id="main-top"]/div[4]/div/div/div/div/div/div/div[2]/div[2]/text()')[0]
                seller.votes = seller.votes.replace("avaliações", "").strip()
                seller.votes = seller.votes.replace(".", "")
                seller.votes = int(seller.votes)
            except:
                seller.rating = ""
                seller.votes = ""

            #usado TRY pois alguns logistas não tem produtos
            try:
                seller.products = tree.xpath('//*[@id="sort-bar"]/div/aside/div/div[1]/span/text()')[0]
                seller.products = seller.products.replace("produtos", "").strip()
                seller.products = seller.products.replace(".", "")
                seller.products = int(seller.products)
            except:
                seller.products = ""

            categoriesName = tree.xpath('//*[@id="collapse-categorias"]/ul/li/a/span/text()')
            categoriesCount = tree.xpath('//*[@id="collapse-categorias"]/ul/li/a/@data-results-count') 
            
            #monta json das categorias
            seller.categories = [] #bugfix, limpando a cada iteracao, em teoria nao precisava pois seller = Seller() tinha que vir limpo 
            for i in range(len(categoriesName)):
                seller.categories.append({
                    "name": categoriesName[i],
                    "count": int(categoriesCount[i])
                })

            #insere dados do seller no json
            sellersJSON[idx]['ecomm_info'].update({
                "name": seller.name,
                "cnpj": seller.cnpj,
                "rating": seller.rating,
                "votes": seller.votes,
                "products": seller.products,
                "categories": seller.categories
            })

            print(str(idx) + ": " + seller.name)
            # a cada X sellers , ou se acabar os sellers, salvamos o arquivo
            saveControl = saveControl + 1
            if(saveControl >= 10):
                print("salvando...")
                saveControl = 0
                f.save_file("data_sellers", "data_sellers_letter_" + letter + ".json", json.dumps(sellersJSON))  
        except:
            print("ERRO NA LEITURA DO SELLER NA LETRA '"+ letter+ "': " + url)
            return
 

    f.save_file("data_sellers", "data_sellers_letter_" + letter + ".json", json.dumps(sellersJSON))  
    print("salvo dados dos sellers da letra " + letter)
    u.endline()
    return sellersJSON