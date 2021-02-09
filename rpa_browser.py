# web element identifier can be XPath selector, CSS selector or
# attributes id, name, class, title, aria-label, text(), href, in decreasing order of priority
import rpa as r

class elementSelector:
    descriptionBtn = ".seller-description > .btn"
    descriptionText = ".seller-modal span pre:nth-of-type(2)"
    ratingScore = ".seller-rating-score"
    ratingVotes = ".seller-rating-votes"
    products = "#sort-bar > div > aside > div > div:nth-child(1) > span"

url = "https://www.americanas.com.br/lojista/webcontinental"


def test():
    print("initializing rpa")
    r.init(chrome_browser = True)


    r.url(url) #navigate tp url address
    r.click(elementSelector.descriptionBtn) #clica no botao de descricao da loja
    
    #leitura do CNPJ que estava na descricao
    cnpj = r.read(elementSelector.descriptionText)
    pos = cnpj.find("Código do lojista:")
    if(pos == -1):
        return
    start_pos = pos + len("Código do lojista:")
    cnpj = cnpj[start_pos:]
    cnpj = cnpj.strip()

    votes = r.read(elementSelector.ratingVotes)
    votes = votes.replace("avaliações", "")
    votes = votes.strip()
    score = r.read(elementSelector.ratingScore)
    score = score.strip()
    products = r.read(elementSelector.products)
    products = products.replace("avaliações", "")
    products = products.strip()
    

    print(cnpj, votes, score, products)
    r.wait(3)
    r.close()
    print("closed rpa")


test()