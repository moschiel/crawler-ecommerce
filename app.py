#! /usr/bin/env python3
import crawler


def main():
    start_letter = 0
    #count = 1 #c.MAX_ABAS
    sellersPerTabUrls = crawler.getSellersByLetterUrls(start_letter)
    #crawler.getSellersData(sellersPerTabUrls)


if __name__ == '__main__':
    main()