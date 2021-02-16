import utils as u
import constants as c

#import lxml.html as parser
#import requests
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait as webWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from time import sleep
import file_manager as f
import json
import urllib

logId = '[Google]:'
    
def getGoogleData(letter):
    letter = u.NumberToLetter(letter)
    print (logId + "BUSCANDO SELLERS DA 'Americanas', LETRA: " + letter)
    #verifica se existe arquivo
    sellersJSON = f.read_file("data_sellers", "data_sellers_letter_" + letter + ".json")
    if(sellersJSON != False ):
        sellersJSON = json.loads(sellersJSON)
    else:
        print(logId + 'arquivo "data_sellers_letter_' + letter + '.json" não encontrado')
        return False

    #verifica se esse arquivo já não esta 100% coletado
    completed = True
    matchCount = 0
    for idx in range(len(sellersJSON)): 
        if("google" not in sellersJSON[idx]):
            completed = False    
            break
        elif("rating" in sellersJSON[idx]["google"]):
            matchCount = matchCount + 1
    if completed:
        print(logId + "carregado " + str(matchCount) + " status de sellers da 'Americanas', letra: " + letter)
        u.endline()
        return sellersJSON

    driver = Chrome(executable_path='./chromedriver88__linux64/chromedriver')

    matchCount = 0
    saveControl = 0
    nameSelector = "div.SPZz6b > h2 > span"
    ratingSelector = "span.Aq14fc"
    votesSelector = "span.hqzQac > span > a > span"

    for idx in range(len(sellersJSON)):
        if("google" in sellersJSON[idx]):    
            # pula sellers ja coletados 
            # print(str(idx) + "(skipped)")
            continue

        search_name = sellersJSON[idx]["americanas"]["name"]
        search_name_url = urllib.parse.quote(search_name)
        search_url = 'https://www.google.com/search?q=' + search_name_url
        #if(True): 
        try:
            driver.get(search_url)
            sleep(4) #delay pra carregar elementos dinâmicos da pagina 
            
            if(len(driver.find_elements_by_css_selector(nameSelector)) == 0 or
               len(driver.find_elements_by_css_selector(ratingSelector)) == 0 or
               len(driver.find_elements_by_css_selector(votesSelector)) == 0):
                print("continue")
                continue

            name = driver.find_element_by_css_selector(nameSelector).text
            rating = driver.find_element_by_css_selector(ratingSelector).text
            rating = float(rating.replace(",", "."))
            votes = driver.find_element_by_css_selector(votesSelector).text
            votes = votes.replace("comentário no Google", "")
            votes = votes.replace("comentários no Google", "")
            votes = int(votes)
            print(idx, name, rating, votes)
            #driver.close()
            #return
        #else: 
        except:
            print("ERRO")
            driver.close()
            return False

    driver.close()
        





#estamos pesquisando no reclame aqui, usando os nomes de empresa da americanas
#mas o idela serial usar os nomes/razão-social da receita federal
def blabla(letter):
    letter = u.NumberToLetter(letter)
    print (logId + "BUSCANDO SELLERS DA 'Americanas', LETRA: " + letter)
    #verifica se existe arquivo
    sellersJSON = f.read_file("data_sellers", "data_sellers_letter_" + letter + ".json")
    if(sellersJSON != False ):
        sellersJSON = json.loads(sellersJSON)
    else:
        print(logId + 'arquivo "data_sellers_letter_' + letter + '.json" não encontrado')
        return False

    #verifica se esse arquivo já não esta 100% coletado
    completed = True
    matchCount = 0
    for idx in range(len(sellersJSON)): 
        if("google" not in sellersJSON[idx]):
            completed = False    
            break
        elif("rating" in sellersJSON[idx]["google"]):
            matchCount = matchCount + 1
    if completed:
        print(logId + "carregado " + str(matchCount) + " status de sellers da 'Americanas', letra: " + letter)
        u.endline()
        return sellersJSON
    
    matchCount = 0
    saveControl = 0
    for idx in range(len(sellersJSON)):
        if("google" in sellersJSON[idx]):    
            # pula sellers ja coletados 
            # print(str(idx) + "(skipped)")
            continue

        search_name = sellersJSON[idx]["americanas"]["name"]
        search_name_url = urllib.parse.quote(search_name)
        search_url = 'https://www.google.com/search?q=' + search_name_url
        if(True): #try:
            while (True): #emula Do-While - enquanto status==202, repita
                sleep(c.REQUEST_INTERVAL) #delay pra evitar detecção de requests massivos
                page = requests.get(search_url, headers = c.HEADERS_GOOGLE(search_name_url))
                if(page.status_code != 202):
                    break
                else:
                    print("Re-try Status: " + str(page.status_code))

            if(page.status_code != 200):
                print(logId + "ERRO NA LEITURA DO SELLER " + search_name + " , STATUS CODE: " + str(page.status_code))
                return False

            tree = parser.fromstring(page.content)
            rating = tree.xpath('//*[@id="rhs"]/div/div[1]/div/div[1]/div/div[1]/div[3]/div[2]/div/div/span[1]')
            votes = tree.xpath('//*[@id="rhs"]/div/div[1]/div/div[1]/div/div[1]/div[3]/div[2]/div/div/span[2]/span/a/span/@text()')

            print(idx, rating, votes)
            u.endline()
            return

            #o conteudo dessa pagina é um JSON
            resultJSON = json.loads(page.content)
            if('companies' not in resultJSON):
                print(logId + "ERRO NA LEITURA DO JSON")
                return False

            match = False
            if(len(resultJSON['companies']) > 0):
                search = sellersJSON[idx]["americanas"]
                search["name"] = search["name"].lower()
                shortname = search["url"][38:]

                #pegamos apenas o primeiro resultado da busca
                result = resultJSON["companies"][0]
                result["companyName"] = result["companyName"].lower()
                result["fantasyName"] = result["fantasyName"].lower()

                #comparamos resultados
                #OBS: daria pra entrar na pagina do primeiro resultado, e pegar CNPJ de la
                #     mas seria um resquest a mais, vamos comparar só o nome mesmo
                if( search["name"] == result["companyName"] or 
                    search["name"] == result["fantasyName"] or
                    shortname == result["shortname"]
                    ):
                    #insere url no JSON
                    result.update({"url":'https://www.reclameaqui.com.br/empresa/'+result["shortname"]})
                    #insere resultado da busca no JSON final
                    sellersJSON[idx].update({
                        "reclameAqui": result
                    }) 
                    match = True
                    matchCount = matchCount + 1
            
            # se não encontrado, inserimos o parametro mesmo que vazio, 
            # só para assim sabermos que ja tentamos este seller
            if(not match):
                sellersJSON[idx].update({
                    "reclameAqui": {}
                }) 

            print(str(idx) + ', match:' + str(match) + ', ' +sellersJSON[idx]['americanas']['name'])
            
            # a cada X paginas ou se acabar os sellers, salvamos o arquivo
            saveControl = saveControl + 1
            if(saveControl >= 10):
                print("salvando...")
                saveControl = 0
                f.save_file("data_sellers", "data_sellers_letter_" + letter + ".json", json.dumps(sellersJSON))  
  
        else: #except:
            print(logId + "ERRO NO INDEX: " + str(idx) + ", SELLER: " + sellersJSON[idx]['americanas']['name'])
            u.endline()
            return False

    f.save_file("data_sellers", "data_sellers_letter_" + letter + ".json", json.dumps(sellersJSON))  
    print(logId + "salvo status de " + str(matchCount) + " sellers da letra " + letter)
    u.endline()
    return sellersJSON
