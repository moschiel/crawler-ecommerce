#! /usr/bin/env python3
import crawler_ecomm


def main():
    letter = 0
    crawler_ecomm.getSellersByLetterUrls(letter)
    crawler_ecomm.getSellersData(letter)

if __name__ == '__main__':
    main()