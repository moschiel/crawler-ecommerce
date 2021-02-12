def getReclameAqui(letter):
    letter = u.NumberToLetter(letter)
    print ("COLETANDO ReclameAqui dos SELLERS DA LETRA " + letter)

    #verifica se existe arquivo, e continua coleta de onde parou
    sellersJSON = f.read_file("data_sellers", "data_sellers_letter_" + letter + ".json")
    sellerIndex = f.read_file("data_sellers", "data_sellers_letter_" + letter + "_last_recAqui.txt")