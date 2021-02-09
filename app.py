#! /usr/bin/env python3
import crawler


def main():
    start_tab = 0
    count = 1 #c.MAX_ABAS
    tabUrls = crawler.setTabUrls(start_tab, count)
    pagesPerTabUrls = crawler.getPagesPerTabUrls(tabUrls)
    sellersPerTabUrls = crawler.getSellersPerTabUrls(pagesPerTabUrls)
    crawler.getSellersData(sellersPerTabUrls)


if __name__ == '__main__':
    main()