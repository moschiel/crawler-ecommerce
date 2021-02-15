#! /usr/bin/env python3
# como usar pip no python3 para Ubuntu
# python3 -m pip install UMA_LIB_QUALQUER

import crawler_americanas as americanas
import crawler_reclameaqui as reclameaqui
import crawler_google as google


def main():
    letter = 24
    if americanas.getSellersUrls(letter) != False:
        if americanas.getSellersData(letter) != False:
            reclameaqui.getReclameAquiData(letter)
            google.getTest(letter)

if __name__ == '__main__':
    main()