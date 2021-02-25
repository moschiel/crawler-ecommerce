import utils as u
import constants as c
import lxml.html as parser
import requests
from time import sleep
import file_manager as f
import json
import urllib

logId = '[ReclameAqui]:'

#estamos pesquisando no reclame aqui, usando os nomes de empresa da americanas
#mas o idela serial usar os nomes/razão-social da receita federal

def getReclameAquiData(letter):
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
        if("reclameAqui" not in sellersJSON[idx]):
            completed = False    
            break
        elif("status" in sellersJSON[idx]["reclameAqui"]):
            matchCount = matchCount + 1
    if completed:
        print(logId + "carregado " + str(matchCount) + " status de sellers da 'Americanas', letra: " + letter)
        u.endline()
        return sellersJSON
    
    matchCount = 0
    saveControl = 0
    for idx in range(len(sellersJSON)):
        if("reclameAqui" in sellersJSON[idx]):    
            # pula sellers ja coletados 
            # print(str(idx) + "(skipped)")
            if("status" in sellersJSON[idx]["reclameAqui"]):
                matchCount = matchCount + 1
            continue

        search_name = sellersJSON[idx]["americanas"]["name"]
        search_name_url = urllib.parse.quote(search_name)
        search_url = 'https://iosearch.reclameaqui.com.br/raichu-io-site-search-v1/companies/search/' + search_name_url
        
        try:
            while (True): #emula Do-While - enquanto status==202, repita
                sleep(c.REQUEST_INTERVAL) #delay pra evitar detecção de requests massivos
                page = requests.get(search_url, headers=c.HEADERS_RECLAMEAQUI)
                if(page.status_code != 202):
                    break
                else:
                    print("Re-try Status: " + str(page.status_code))

            if(page.status_code != 200):
                print(logId + "ERRO NA LEITURA DO SELLER " + search_name + " , STATUS CODE: " + str(page.status_code))
                return False

            #o conteudo dessa pagina é um JSON
            resultJSON = json.loads(page.content)
            if('companies' not in resultJSON):
                print(logId + "ERRO NA LEITURA DO JSON")
                return False

            match = False
            if(len(resultJSON['companies']) > 0):
                search = sellersJSON[idx]["americanas"]
                shortname = search["url"][38:]
                searchQSA = ""
                if('qsa' in sellersJSON[idx]):
                    if ('cnpj' in sellersJSON[idx]['qsa']):
                        searchQSA = sellersJSON[idx]['qsa']

                #pegamos apenas o primeiro resultado da busca
                result = resultJSON["companies"][0]

                #comparamos resultados
                #OBS: daria pra entrar na pagina do primeiro resultado, e pegar CNPJ de la
                #     mas seria um resquest a mais, vamos comparar só o nome mesmo
                if( u.compareAlphanumeric( search["name"], result["companyName"] ) or 
                    u.compareAlphanumeric( search["name"], result["fantasyName"] ) or
                    u.compareAlphanumeric( shortname, result["shortname"] )
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

            print(str(idx) + ', match:' + str(match) + ', ' + search_name)
            
            # a cada X paginas ou se acabar os sellers, salvamos o arquivo
            saveControl = saveControl + 1
            if(saveControl >= 10):
                print("salvando...")
                saveControl = 0
                f.save_file("data_sellers", "data_sellers_letter_" + letter + ".json", json.dumps(sellersJSON))  
  
        except:
            print(logId + "ERRO NO INDEX: " + str(idx) + ", SELLER: " + search_name)
            u.endline()
            return False

    f.save_file("data_sellers", "data_sellers_letter_" + letter + ".json", json.dumps(sellersJSON))  
    print(logId + "salvo status de " + str(matchCount) + " sellers da letra " + letter)
    u.endline()
    return sellersJSON
