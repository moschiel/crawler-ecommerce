#! /usr/bin/env python3
import url_collector

class Seller:
    name = ""
    rating = ""
    numRatings = ""
    numProducts = ""


def getSellersDataPerTab(sellersPerTabUrls):
    print ("COLETANDO DADOS DOS SELLERS DE CADA ABA")
    for sellersUrls in sellersPerTabUrls:
        Sellers = []
        for sellerUrl in sellersUrls:
            try:
                sleep(c.REQUEST_INTERVAL) #delay pra evitar detecção de requests massivos, o que causaria error 403
                page = requests.get("https://www.americanas.com.br/lojista/93-eletronicos", headers=c.HEADERS)
                #page = requests.get("https://www.americanas.com.br/lojista/" + sellerUrl, headers=c.HEADERS) 
                tree = parser.fromstring(page.content)
                print(type(page.content)) 
                print(type(tree))  
                print(type("Ola")) 
                f.save_file("page", "page.txt", str(page.content))
                return 

                #quando a pagina não está funcionando, é retornado "Ops! Página não encontrada"
                result = tree.xpath('//*[@id="content-middle"]/div[4]/div/div/div/div[2]/span[1]/span/span/text()')
                if(len(result) > 0 and result[0].strip() == "Ops!"):
                    print("Ops!")
                    continue
                
                seller = Seller()
                seller.name = tree.xpath() 
                return
            except:
                print("BLA")
                return
            #Sellers.append( )
    return

def main():
    start_tab = 0
    count = 1 #c.MAX_ABAS
    tabUrls = urlCollector.setTabUrls(start_tab, count)
    pagesPerTabUrls = urlCollector.getPagesPerTab(tabUrls)
    sellersPerTabUrls = urlCollector.getSellersPerTab(pagesPerTabUrls)
    #getSellersDataPerTab(sellersPerTabUrls)


if __name__ == '__main__':
    main()