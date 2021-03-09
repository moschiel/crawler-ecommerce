#! /usr/bin/env python3

import crawler_americanas as americanas
import crawler_reclameaqui as reclameaqui
import crawler_google as google
import crawler_qsa as QSA


def main():
    letter = 24 #indice da letra no alfabeto
    if americanas.getSellersUrls(letter) != False:
        if americanas.getSellersData(letter) != False:
            QSA.getSellersQsa(letter)
            reclameaqui.getReclameAquiData(letter)
            google.getGoogleData(letter)

if __name__ == '__main__':
    main()

#comandos terminal
#python3 -m pip install UMA_LIB_QUALQUER
#sudo /opt/lampp/manager-linux-x64.run
#sudo /etc/init.d/apache2 stop



