#! /usr/bin/env python3
import utils as u
import constants as c
import lxml.html as parser
import requests


def setTabUrls(startTab=0, count=0):
    print("SETANDO URLs DE CADA ABA")
    urls = []
    for index in range(count):
        char_tab = u.NumberToLetter(startTab + index)
        url = "https://www.americanas.com.br/mapa-do-site/lojista/f/letra-" + char_tab
        urls.append(url)
        if(c.PRINT_ABA_URL):
            print (url)
    u.endline()
    return urls

def getPagesPerTab(TabUrls):
    print("LENDO URL DE PAGINAS DE CADA ABA")
    pages_per_tab = []
    for tabUrl in TabUrls:
        #read last character
        chr_tab = tabUrl[-1:]
        if(chr_tab == "0"):
            chr_tab = "#"

        print("PAGINAS DA ABA '" + chr_tab + "'")    
        try:
            page = requests.get(tabUrl, headers=c.HEADERS)
            tree = parser.fromstring(page.content)
            page_urls = tree.xpath('//*[@id="summary-pane-'+ chr_tab +'"]/div/div/div/div/ul/li/a/@href')
            page_urls = u.RemoveDuplicates(page_urls) 
            page_urls = u.RemoveIfContain(page_urls, "#")
            for i in range(len(page_urls)):
                if(("pagina" not in page_urls[i]) and ("letra" in page_urls[i])):
                    page_urls[i] += "/pagina-1"
                page_urls[i] = "https://www.americanas.com.br" + page_urls[i]
                print(page_urls[i])
        except:
            page_urls = "except"
            print("ERRO NA LEITURA DE PAGINAS DA ABA '" + chr_tab + "'")
        u.endline() 
    u.endline() 
    return pages_per_tab


start_tab = 0
count = 3 #c.MAX_ABAS
tabUrls = setTabUrls(start_tab, count)
getPagesPerTab(tabUrls)
