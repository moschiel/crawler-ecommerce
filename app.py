#! /usr/bin/env python3

import crawler_americanas as americanas
import crawler_reclameaqui as reclameaqui
import crawler_google as google


def main():
    letter = 24
    if americanas.getSellersUrls(letter) != False:
        if americanas.getSellersData(letter) != False:
            reclameaqui.getReclameAquiData(letter)
            google.getGoogleData(letter)

if __name__ == '__main__':
    main()

#comandos terminal
#python3 -m pip install UMA_LIB_QUALQUER
#sudo /opt/lampp/manager-linux-x64.run
#sudo /etc/init.d/apache2 stop
#ssh rogerm@10.181.194.159
