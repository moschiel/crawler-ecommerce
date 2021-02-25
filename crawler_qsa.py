import utils as u
import constants as c
import file_manager as f
import json
import qsa

logId = '[QSA]:'

def getSellersQsa(letter):
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
        if("qsa" not in sellersJSON[idx]):
            completed = False    
            break
        elif("cnpj" in sellersJSON[idx]["qsa"]):
            matchCount = matchCount + 1
    if completed:
        print(logId + "carregado " + str(matchCount) + " QSA de sellers da 'Americanas', letra: " + letter)
        u.endline()
        return sellersJSON
    
    matchCount = 0
    saveControl = 0
    for idx in range(len(sellersJSON)):
        if("qsa" in sellersJSON[idx]):    
            # pula sellers ja coletados 
            # print(str(idx) + "(skipped)")
            if("cnpj" in sellersJSON[idx]["qsa"]):
                matchCount = matchCount + 1
            continue

        search_name = sellersJSON[idx]["americanas"]["name"]
        search_cnpj = sellersJSON[idx]["americanas"]["cnpj"]
        
        try:
            match = False
            qsaJson = qsa.get_QSA_JSON(search_cnpj)
            if(qsaJson == None):
                print(logId + "ERRO NA LEITURA DO SELLER: " + search_name + " , CNPJ: " + search_cnpj)
                sellersJSON[idx].update({
                    "qsa": {}
                })
                qsa.close()
                return False
            else:
                match = True
                matchCount = matchCount + 1
                sellersJSON[idx].update(qsaJson)
            
            print(str(idx) + ', match:' + str(match) + ', ' + search_name)
            
            # a cada X paginas ou se acabar os sellers, salvamos o arquivo
            saveControl = saveControl + 1
            if(saveControl >= 10):
                print("salvando...")
                saveControl = 0
                f.save_file("data_sellers", "data_sellers_letter_" + letter + ".json", json.dumps(sellersJSON))  
  
        except:
            print(logId + "ERRO NO INDEX: " + str(idx) + ", SELLER: " + search_name + " , CNPJ: " + search_cnpj)
            u.endline()
            qsa.close()
            return False

    qsa.close()
    f.save_file("data_sellers", "data_sellers_letter_" + letter + ".json", json.dumps(sellersJSON))  
    print(logId + "salvo status de " + str(matchCount) + " sellers da letra " + letter)
    u.endline()
    return sellersJSON