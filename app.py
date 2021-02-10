#! /usr/bin/env python3
import crawler


def main():
    letter = 0
    crawler.getSellersByLetterUrls(letter)
    crawler.getSellersData(letter)

if __name__ == '__main__':
    main()