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
            if("rating" in sellersJSON[idx]["google"]):
                matchCount = matchCount + 1
            continue

        search_name = sellersJSON[idx]["americanas"]["name"]
        search_name_url = urllib.parse.quote(search_name)
        search_url = 'https://www.google.com/search?q=' + search_name_url

        try:
            driver.get(search_url)
            sleep(4) #delay pra carregar elementos dinâmicos da pagina 
            
            namesArray = driver.find_elements_by_css_selector(nameSelector)
            ratingsArray = driver.find_elements_by_css_selector(ratingSelector)
            votesArray = driver.find_elements_by_css_selector(votesSelector)

            match = False

            if(len(namesArray) > 0 and len(ratingsArray) > 0 and len(ratingSelector) > 0
                and u.compareAlphanumeric(namesArray[0].text, search_name)):
                
                name = driver.find_element_by_css_selector(nameSelector).text
                rating = driver.find_element_by_css_selector(ratingSelector).text
                rating = float(rating.replace(",", "."))
                votes = driver.find_element_by_css_selector(votesSelector).text
                votes = votes.replace("comentário no Google", "")
                votes = votes.replace("comentários no Google", "")
                votes = int(votes)
                
                sellersJSON[idx].update({
                    "google": {
                        "rating": rating,
                        "votes": votes
                    }
                }) 

                match = True
                matchCount = matchCount + 1

                
            # se não encontrado, inserimos o parametro mesmo que vazio, 
            # só para assim sabermos que ja tentamos este seller
            if(not match):
                sellersJSON[idx].update({
                    "google": {}
                }) 
            
            print(str(idx) + ', match:' + str(match) + ', ' + search_name)

            # a cada X paginas ou se acabar os sellers, salvamos o arquivo
            saveControl = saveControl + 1
            if(saveControl >= 10):
                print("salvando...")
                saveControl = 0
                f.save_file("data_sellers", "data_sellers_letter_" + letter + ".json", json.dumps(sellersJSON))  

        except:
            driver.close()
            print(logId + "ERRO NO INDEX: " + str(idx) + ", SELLER: " + search_name)
            u.endline()
            return False

    driver.close()
    f.save_file("data_sellers", "data_sellers_letter_" + letter + ".json", json.dumps(sellersJSON))  
    print(logId + "salvo status de " + str(matchCount) + " sellers da letra " + letter)
    u.endline()
    return sellersJSON
