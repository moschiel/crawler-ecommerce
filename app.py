#! /usr/bin/env python3
import crawler_americanas as americanas
import crawler_reclameaqui as reclameaqui


def main():
    letter = 24
    if americanas.getSellersUrls(letter) != False:
        if americanas.getSellersData(letter) != False:
            reclameaqui.getReclameAquiData(letter)

if __name__ == '__main__':
    main()