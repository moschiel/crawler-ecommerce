import os
import csv

def createFolder(directory):
    try:
        directory = os.path.join(os.getcwd(), "files", directory) 
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)


def save_file(directory, fileName, txtData):
    # a - will append to the end of the file
    # w - will overwrite any existing content
    try:
        createFolder(directory)
        filePath = os.path.join(os.getcwd(), "files", directory, fileName) 
        with open(filePath, 'w', encoding='utf8') as output:
            output.write(txtData) 
        output.close()  
    except:
        print("ERROR SAVING FILE: " + fileName)

def read_file(directory, fileName):
    filePath = os.path.join(os.getcwd(), "files", directory, fileName)
    if(os.path.exists(filePath)):
        return open(filePath, "r").read()
    return False

def save_csv_file(directory, fileName, csvData):
    # a - will append to the end of the file
    # w - will overwrite any existing content
    try:
        createFolder(directory)
        filePath = os.path.join(os.getcwd(), "files", directory, fileName) 
        with open(filePath, 'w', encoding='utf8') as output:
            writer = csv.writer(output)
            writer.writerows(csvData) 
        output.close()  
    except:
        print("ERROR SAVING FILE: " + fileName)