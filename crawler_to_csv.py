import file_manager as f
import utils as u
import json
import constants as c

colunas_seller = ['cnpj','lojista','nota','votos','produtos','link']
colunas_categoria = []
colunas_google = ['notas', 'votos', 'contato']
colunas_reclame_aqui = ['notas', 'votos']
colunas_qsa = [
    #"cnpj",
    "razao_social",
    "nome_fantasia",
    "situacao",
    "data_situacao",
    "motivo_situacao",
    "cod_nat_juridica",
    "cnae_fiscal",
    "tipo_logradouro",
    "logradouro",
    "numero",
    "complemento",
    "bairro",
    "uf",
    "municipio",
    "cep",
    "ddd_1",
    "telefone_1",
    "ddd_2",
    "telefone_2",
    "email",
    "capital_social",
    "porte",
    "opc_simples",
    "opc_mei"
]

logId = "[CSV]: "

def updateCategoriesList():
    print (logId + "ATUALIZANDO CATEGORIAS: ")
    AllCategories = []
    global colunas_categoria

    for letter in range(c.MAX_LETTER):
        letter = u.NumberToLetter(letter)

        #verifica se existe arquivo
        sellersJSON = f.read_file("data_sellers", "data_sellers_letter_" + letter + ".json")
        if(sellersJSON != False ):
            sellersJSON = json.loads(sellersJSON)
        else:
            print(logId + 'arquivo "data_sellers_letter_' + letter + '.json" não encontrado')
            continue
        
        for seller in sellersJSON:
            if('categories' in seller['americanas']):
                sellerCategories = seller['americanas']['categories']
                for category in sellerCategories:
                    if(category['name'] not in AllCategories):
                        AllCategories.append(category['name'])
        AllCategories.sort()
        f.save_file("categories", "categories.txt", json.dumps(AllCategories)) 
     
        colunas_categoria = AllCategories
        
    print (logId + "Carregado " + str(len(AllCategories)) + ' categorias')
        


def convertToCsv(letter):
    global colunas_categoria
    letter = u.NumberToLetter(letter)
    print (logId + "GERANDO CSV DE SELLERS DA 'Americanas', LETRA: " + letter)

    #verifica se existe arquivo
    sellersJSON = f.read_file("data_sellers", "data_sellers_letter_" + letter + ".json")
    if(sellersJSON != False ):
        sellersJSON = json.loads(sellersJSON)
    else:
        print(logId + 'arquivo "data_sellers_letter_' + letter + '.json" não encontrado')
        return False

    #monta celulas 'mergeadas' da AMERICANAS
    merged_seller = []
    for col in colunas_seller:
        merged_seller.append('')
    merged_seller[0] = 'AMERICANAS'
    #monta celulas 'mergeadas' das CATEGORIAS
    merged_categoria = []
    for col in colunas_categoria:
        merged_categoria.append('')
    merged_categoria[0] = 'CATEGORIAS'

    #monta colunas header
    csvData = []
    csvData.append( merged_seller + merged_categoria)
    csvData.append(colunas_seller + colunas_categoria)

    for seller in sellersJSON:
        csvData.append( sellerToCsv(seller) + categoriesToCsv(seller) )
    
    f.save_csv_file('csv_sellers', 'sellers_' + letter + '.csv', csvData)

def sellerToCsv(sellerJson):
    sellerEcomm = sellerJson['americanas']
    sellerCSV = []
    sellerCSV.append( sellerEcomm['cnpj'] ) #coluna cnpj
    sellerCSV.append( sellerEcomm['name'] ) #coluna lojista
    sellerCSV.append( str(sellerEcomm['rating']) ) #coluna nota
    sellerCSV.append( str(sellerEcomm['votes']) ) #coluna votos
    sellerCSV.append( str(sellerEcomm['products']) ) #coluna produtos 
    sellerCSV.append( sellerEcomm['url'] ) #coluna link

    return sellerCSV

def categoriesToCsv(sellerJson):
    global colunas_categoria
    #inicializa array
    categoriasCSV = [''] * len(colunas_categoria)

    sellerCategorias = sellerJson['americanas']['categories']
    for categoria in sellerCategorias:
        if(categoria['name'] in colunas_categoria):
            idx = colunas_categoria.index(categoria['name'])
            categoriasCSV[idx] = categoria['count']
        else:
            print(logId + "Error, não encontrado categoria '" + categoria['name'] + "'")

    return categoriasCSV


if __name__ == '__main__':
    updateCategoriesList()
    convertToCsv(24)