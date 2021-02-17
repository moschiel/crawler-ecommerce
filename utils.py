import unicodedata

def endline():
    print("")


def RemoveDuplicates(data_array):
    out_array = [] 
    for val in data_array: 
        if val not in out_array: 
            out_array.append(val)
    return out_array 

def RemoveIfContain(data_array, selector):
    out_array = [] 
    for val in data_array: 
        if selector not in val: 
            out_array.append(val)
    return out_array 

def NumberToLetter(num):
    if(num==0):
        return '#'
    else:
        return chr(ord('a')+ num - 1) 

def compareAlphanumeric(text1, text2):
    text1 = convertToAlphanumeric(text1)
    text2 = convertToAlphanumeric(text2)
    return (text1 == text2)

def removeAccentuation(text):
    # peça ótimo péssimo não é tão às
    text = unicodedata.normalize("NFD", text)
    # b'peca otimo pessimo nao e tao as'
    text = text.encode("ascii", "ignore")
    # peca otimo pessimo nao e tao as
    text = text.decode("utf-8")
    return text

def convertToAlphanumeric(text):
    text = removeAccentuation(text)
    text = text.lower()
    if(not text.isalnum()): #string is not alphanumeric
        for ch in text: 
            if(not ch.isalnum()): #character is not alphanumeric
                text = text.replace(ch, " ")
        while(text.find("  ") != -1):
            text = text.replace("  ", " ")
    text = text.strip()
    return text     
    