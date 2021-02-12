#! /usr/bin/env python3
import crawler_americanas as americanas


def main():
    letter = 24
    if americanas.getSellersByLetterUrls(letter) != False:
        americanas.getSellersData(letter)

if __name__ == '__main__':
    main()