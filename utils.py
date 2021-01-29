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
        return '0'
    else:
        return chr(ord('a')+ num - 1) 