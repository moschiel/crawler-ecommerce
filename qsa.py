import mysql.connector

class EnumQSA:
    cnpj = 0
    razao_social = 2
    nome_fantasia = 3
    situacao = 4
    data_situacao = 5
    motivo_situacao = 6
    cod_nat_juridica = 10
    cnae_fiscal = 12
    tipo_logradouro = 13
    logradouro = 14
    numero = 15
    complemento = 16
    bairro = 17
    cep = 18
    uf = 19
    municipio = 21
    ddd_1 = 22
    telefone_1 = 23
    ddd_2 = 24
    telefone_2 = 25
    email = 28
    capital_social = 30
    porte = 31
    opc_simples = 32

def GET_SITUACAO(codigo):
    if codigo == "01": return "01-NULA"
    elif codigo == "02": return "02-ATIVA"
    elif codigo == "03": return "03-SUSPENSA"
    elif codigo == "04": return "04-INAPTA"
    elif codigo == "05": return "05-BAIXADA"
    else: return codigo

def GET_MOTIVO_SITUACAO(codigo):
    if codigo == "01": return "01-EXTINÇÃO POR ENCERRAMENTO LIQUIDAÇÃO VOLUNTÁRIA"
    elif codigo == "02": return "02-INCORPORAÇÃO"
    elif codigo == "03": return "03-FUSÃO"
    elif codigo == "04": return "04-CISÃO TOTAL" 
    elif codigo == "05": return "05-ENCERRAMENTO DA FALÊNCIA"
    elif codigo == "06": return "06-ENCERRAMENTO DA LIQUIDAÇÃO"
    elif codigo == "07": return "07-ELEVAÇÃO A MATRIZ"
    elif codigo == "08": return "08-TRANSPASSE"
    elif codigo == "09": return "09-NÃO INÍCIO DE ATIVIDADE"
    elif codigo == "10": return "10-EXTINÇÃO PELO ENCERRAMENTO DA LIQUIDAÇÃO JUDICIAL"
    elif codigo == "11": return "11-ANULAÇÃO POR MULTICIPLIDADE"
    elif codigo == "12": return "12-ANULAÇÃO ONLINE DE OFICIO"
    elif codigo == "13": return "13-OMISSA CONTUMAZ"
    elif codigo == "14": return "14-OMISSA NÃO LOCALIZADA"
    elif codigo == "15": return "15-INEXISTENTE DE FATO"
    elif codigo == "16": return "16-ANULAÇÃO POR VÍCIOS"
    elif codigo == "17": return "17-BAIXA INICIADA E AINDA NÃO DEFERIDA"
    elif codigo == "18": return "18-INTERRUPÇÃO TEMPORÁRIA DAS ATIVIDADES"
    elif codigo == "19": return "19-OMISSO DE DIRPJ ATÉ 5 EXERCÍCIOS"
    elif codigo == "20": return "20-EM CONDIÇÃO DE INAPTIDÃO"
    elif codigo == "21": return "21-PEDIDO DE BAIXA INDEFERIDA"
    elif codigo == "22": return "22-RESTABELECIMENTO COM CERTIDÃO POSITIVA COM EFEITO DE NEGATIVA"
    elif codigo == "23": return "23-COM PENDÊNCIA FISCAL"
    elif codigo == "24": return "24-POR EMISSÃO CERTIDÃO NEGATIVA"
    elif codigo == "25": return "25-CERTIDÃO POSITIVA COM EFEITO DE NEGATIVA"
    elif codigo == "26": return "26-IRREGULARIDADE DE PAGAMENTO"
    elif codigo == "27": return "27-IRREGULARIDADE DE RECOLHIMENTO E EXIGIBILIDADE SUSPENSA"
    elif codigo == "28": return "28-TRANSFERÊNCIA FILIAL CONDIÇÃO MATRIZ"
    elif codigo == "29": return "29-AGUARDANDO CONF. DE DIRPJ/DIPJ"
    elif codigo == "30": return "30-ANR - AGUARDANDO CONF. DE DIRPJ/DIPJ"
    elif codigo == "31": return "31-EXTINÇÃO DA FILIAL"
    elif codigo == "32": return "32-INEXISTENTE DE FATO ADE/COSAR"
    elif codigo == "33": return "33-TRANSFERÊNCIA DO ÓRGÃO LOCAL A CONDIÇÃO DE FILIAL DO ÓRGÃO REGIONAL"
    elif codigo == "34": return "34-ANULAÇÃO DE INSCRIÇÃO INDEVIDA"
    elif codigo == "35": return "35-EMPRESA ESTRANGEIRA AGUARDANDO DOCUMENTAÇÃO"
    elif codigo == "36": return "36-PRÁTICA IRREGULAR DE OPERAÇÃO DE COMERCIO EXTERIOR"
    elif codigo == "37": return "37-BAIXA DE PRODUTOR RURAL"
    elif codigo == "38": return "38-BAIXA DEFERIDA PELA RFB AGUARDANDO ANALISE DO CONVENENTE"
    elif codigo == "39": return "39-BAIXA DEFERIDA PELA RFB E INDEFERIDA PELO CONVENENTE"
    elif codigo == "40": return "40-BAIXA INDEFERIDA PELA RFB E AGUARDANDO ANALISE DO CONVENENTE"
    elif codigo == "41": return "41-BAIXA INDEFERIDA PELA RFB E DEFERIDA PELO CONVENENTE"
    elif codigo == "42": return "42-BAIXA INDEFERIDA PELA RFB E SEFIN, AGUARDANDO ANALISE SEFAZ"
    elif codigo == "43": return "43-BAIXA DEFERIDA PELA RFB, AGUARDANDO ANALISE DA SEFAZ E INDEFERIDA PELA SEFIN"
    elif codigo == "44": return "44-BAIXA DEFERIDA PELA RFB E SEFAZ, AGUARDANDO ANALISE SEFIN"
    elif codigo == "45": return "45-BAIXA DEFERIDA PELA RFB, AGUARDANDO ANALISE DA SEFIN E INDEFERIDA PELA SEFAZ"
    elif codigo == "46": return "46-BAIXA DEFERIDA PELA RFB E SEFAZ E INDEFERIDA PELA SEFIN"
    elif codigo == "47": return "47-BAIXA DEFERIDA PELA RFB E SEFIN E INDEFERIDA PELA SEFAZ"
    elif codigo == "48": return "48-BAIXA INDEFERIDA PELA RFB, AGUARDANDO ANALISE SEFAZ E DEFERIDA PELA SEFIN"
    elif codigo == "49": return "49-BAIXA INDEFERIDA PELA RFB, AGUARDANDO ANALISE DA SEFAZ E INDEFERIDA PELA SEFIN"
    elif codigo == "50": return "50-BAIXA INDEFERIDA PELA RFB, DEFERIDA PELA SEFAZ E AGUARDANDO ANALISE DA SEFIN"
    elif codigo == "51": return "51-BAIXA INDEFERIDA PELA RFB E SEFAZ, AGUARDANDO ANALISE DA SEFIN"
    elif codigo == "52": return "52-BAIXA INDEFERIDA PELA RFB, DEFERIDA PELA SEFAZ E INDEFERIDA PELA SEFIN"
    elif codigo == "53": return "53-BAIXA INDEFERIDA PELA RFB E SEFAZ E DEFERIDA PELA SEFIN"
    elif codigo == "54": return "54-BAIXA - TRATAMENTO DIFERENCIADO DADO AS ME E EPP (LEI COMPLEMENTAR NUMERO 123/2006)"
    elif codigo == "55": return "55-DEFERIDO PELO CONVENENTE, AGUARDANDO ANALISE DA RFB"
    elif codigo == "60": return "60-ARTIGO 30, VI, DA IN 748/2007"
    elif codigo == "61": return "61-INDICIO INTERPOS. FRAUDULENTA"
    elif codigo == "62": return "62-FALTA DE PLURALIDADE DE SOCIOS"
    elif codigo == "63": return "63-OMISSÃO DE DECLARAÇÕES"
    elif codigo == "64": return "64-LOCALIZAÇÃO DESCONHECIDA"
    elif codigo == "66": return "66-INAPTIDÃO"
    elif codigo == "67": return "67-REGISTRO CANCELADO"
    elif codigo == "70": return "70-ANULAÇÃO POR NÃO CONFIRMADO ATO DE REGISTRO DO MEI NA JUNTA COMERCIAL"
    elif codigo == "71": return "71-INAPTIDÃO (LEI 11.941/2009 ART.54)"
    elif codigo == "72": return "72-DETERMINAÇÃO JUDICIAL"
    elif codigo == "73": return "73-OMISSÃO CONTUMAZ"
    elif codigo == "74": return "74-INCONSISTÊNCIA CADASTRAL"
    elif codigo == "80": return "80-BAIXA REGISTRADA NA JUNTA, INDEFERIDA NA RFB"
    else: return codigo

class QsaDB:
    connection = None
    cursor = None
    tables = []
    def init(self):
        self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="qsa"
            )
        self.cursor = self.connection.cursor()
        self.get_Tables()
        print("Initialized QSA DataBase Connection")

    def close(self):
        self.cursor.close()
        self.cursor = None
        self.connection.close()
        self.connection = None
        print("Closed QSA DataBase Connection")

    def isConnected(self):
        if (self.connection != None and self.cursor != None):
            return True
        else:
            return False

    def get_Tables(self):
        if(not self.isConnected()):
            self.init()

        self.cursor.execute("SHOW TABLES")
        self.tables = []
        for (table_name, ) in self.cursor:
            self.tables.append(table_name)


#INSTANCIA QSA DATABASE CONNECTION
QSAconn = QsaDB()

def convertToNum(text):
    if(text != "" and text.isnumeric()):
        return int(text)
    return ""

def close():
    QSAconn.close()

def get_QSA_JSON(cnpj):
    if(not QSAconn.isConnected()):
        QSAconn.init()

    for table in QSAconn.tables:
        if(table == "empresas"): #codigo temporario
            continue
        QSAconn.cursor.execute("SELECT * FROM {} WHERE cnpj='{}' LIMIT 1".format(table, cnpj))
        queryResult = QSAconn.cursor.fetchone()
        if(queryResult != None):
            return {
                "qsa": {
                    "cnpj": queryResult[EnumQSA.cnpj],
                    "razao_social": queryResult[EnumQSA.razao_social],
                    "nome_fantasia": queryResult[EnumQSA.nome_fantasia],
                    "situacao": GET_SITUACAO(queryResult[EnumQSA.situacao]),
                    "data_situacao": queryResult[EnumQSA.data_situacao],
                    "motivo_situacao": GET_MOTIVO_SITUACAO(queryResult[EnumQSA.motivo_situacao]),
                    "cod_nat_juridica": convertToNum(queryResult[EnumQSA.cod_nat_juridica]),
                    "cnae_fiscal": convertToNum(queryResult[EnumQSA.cnae_fiscal]),
                    "tipo_logradouro": queryResult[EnumQSA.tipo_logradouro],
                    "logradouro": queryResult[EnumQSA.logradouro],
                    "numero": queryResult[EnumQSA.numero],
                    "complemento": queryResult[EnumQSA.complemento],
                    "bairro": queryResult[EnumQSA.bairro],
                    "uf": queryResult[EnumQSA.uf],
                    "municipio": queryResult[EnumQSA.municipio],
                    "cep": queryResult[EnumQSA.cep],
                    "ddd_1": queryResult[EnumQSA.ddd_1],
                    "telefone_1": queryResult[EnumQSA.telefone_1],
                    "ddd_2": queryResult[EnumQSA.ddd_2],
                    "telefone_2": queryResult[EnumQSA.telefone_2],
                    "email": queryResult[EnumQSA.email],
                    "capital_social": queryResult[EnumQSA.capital_social],
                    "porte": convertToNum(queryResult[EnumQSA.porte]),
                    "opc_simples": convertToNum(queryResult[EnumQSA.opc_simples])
                }
            }
        else:
            continue
    return None


#res = get_QSA_JSON('01888722000197')
#print(res)
#QSAconn.close()
