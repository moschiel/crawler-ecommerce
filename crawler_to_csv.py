import file_manager as f
import utils as u
import json

merged_seller = ['AMERICANAS','','','','','']
colunas_seller = ['cnpj','lojista','nota','votos','produtos','link']

#os nomes dessa coluna devem ser igual do json
colunas_categoria = [
    "acabamentos para pisos e revestimentos",
    "acessórios para monitores cardíacos",
    "adesivos, fitas e colas",
    "agro, indústria e comércio",
    "alimentos",
    "ar-condicionado e aquecedores",
    "artesanato",
    "artigos de festas",
    "automotivo",
    "balaustre de madeira",
    "bebidas",
    "bebês",
    "beleza e perfumaria",
    "brinquedos",
    "caibro de madeira",
    "cal",
    "calhas",
    "cama, mesa e banho",
    "capacetes",
    "casa e construção",
    "celulares e smartphones",
    "cerâmica hidráulica",
    "construção",
    "corante",
    "corrimão de madeira",
    "cronômetros e pedômetros",
    "câmeras e filmadoras",
    "decoração",
    "dicionários",
    "eletrodomésticos",
    "eletroportáteis",
    "enfeites de natal",
    "esporte e lazer",
    "ferros e aços",
    "filmes e séries",
    "flores",
    "food delivery",
    "forro",
    "games",
    "gesso",
    "gift card",
    "informática",
    "informática e acessórios",
    "instrumentos musicais",
    "isolantes",
    "ladrilhos de vidro",
    "ladrilhos hidráulicos",
    "livros"
]

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
def convertToCsv(letter):
    letter = u.NumberToLetter(letter)
    print (logId + "GERANDO CSV DE SELLERS DA 'Americanas', LETRA: " + letter)

    #verifica se existe arquivo
    sellersJSON = f.read_file("data_sellers", "data_sellers_letter_" + letter + ".json")
    if(sellersJSON != False ):
        sellersJSON = json.loads(sellersJSON)
    else:
        print(logId + 'arquivo "data_sellers_letter_' + letter + '.json" não encontrado')
        return False

    #monta colunas header
    csvData = []
    csvData.append( merged_seller )
    #csvData[0] += merged_categoria
    #csvData[0] += merged_google
    #csvData[0] += merged_reclame_aqui
    #csvData[0] += merged_qsa
    csvData.append(colunas_seller)
    #csvData[0] += colunas_categoria
    #csvData[0] += colunas_google
    #csvData[0] += colunas_reclame_aqui
    #csvData[0] += colunas_qsa

    for seller in sellersJSON:
        csvData.append( sellerToCsv(seller) )
    
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

    #categoriesEcomm = sellerEcomm['categories']
    #for idx in range(len(colunas_categoria)):

    return sellerCSV



convertToCsv(24)