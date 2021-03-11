import mysql.connector
import qsa_codes as codes

#posição das colunas do QSA da Receita
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
    opc_mei = 35

class QsaDB:
    connection = None
    cursor = None
    tables = []
    def init(self):
        self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="qsa",
                charset="utf8"
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
                    #"cnpj": queryResult[EnumQSA.cnpj],
                    "razao_social": queryResult[EnumQSA.razao_social],
                    "nome_fantasia": queryResult[EnumQSA.nome_fantasia],
                    "situacao": codes.SITUACAO(queryResult[EnumQSA.situacao]),
                    "data_situacao": queryResult[EnumQSA.data_situacao],
                    "motivo_situacao": codes.MOTIVO_SITUACAO(queryResult[EnumQSA.motivo_situacao]),
                    "cod_nat_juridica": codes.NATUREZA_JURIDICA(queryResult[EnumQSA.cod_nat_juridica]),
                    "cnae_fiscal": codes.CNAE(queryResult[EnumQSA.cnae_fiscal]),
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
                    "porte": codes.PORTE(queryResult[EnumQSA.porte]),
                    "opc_simples": codes.OPC_SIMPLES(queryResult[EnumQSA.opc_simples]),
                    "opc_mei":  codes.OPC_MEI(queryResult[EnumQSA.opc_mei])
                }
            }
        else:
            continue
    return None


#res = get_QSA_JSON('10365665000152')
#print(res)
#QSAconn.close()