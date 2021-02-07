# web element identifier can be XPath selector, CSS selector or
# attributes id, name, class, title, aria-label, text(), href, in decreasing order of priority
import rpa as r

class pageElements:
    description = ".seller-description > .btn"
    
url = "https://www.americanas.com.br/lojista/3n-s-lasers"



print("initializing rpa")

r.init(chrome_browser = True)
r.url(url)
r.click(pageElements.description)
r.wait(5)
r.close()
print("closed rpa")