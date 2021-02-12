def getReclameAquiUrls(letter):
    letter = u.NumberToLetter(letter)
    print ("[Reclame Aqui]COLETANDO URL DOS SELLERS DA LETRA " + letter)

    #verifica se existe arquivo
    sellersJSON = f.read_file("data_sellers", "data_sellers_letter_" + letter + ".json")
    if(sellersJSON != False ):
        sellersJSON = json.loads(sellersJSON)
    else:
        print('[Reclame Aqui]arquivo "data_sellers_letter_' + letter + '.json" não encontrado')
        return
    
    saveControl = 0
    for idx in range(len(sellersJSON)):
        if("name" not in sellersJSON[idx]["americanas"]):    
            # pula seller se não tiver os dados para busca 
            print(str(idx) + "(skipped - seller name not found)")
            continue
        
        search_url='https://www.reclameaqui.com.br/busca/?q='+sellersJSON[idx]['americanas']['name'].lower()
        print(search_url)
        return
