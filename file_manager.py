import os

def createFolder(directory):
    try:
        directory = os.path.join(os.getcwd(), "files", directory) 
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)


def save_text_file(directory, fileName, txtData):
    # a - will append to the end of the file
    # w - will overwrite any existing content
    try:
        createFolder(directory)
        filePath = os.path.join(os.getcwd(), "files", directory, fileName) 
        with open(filePath, 'w') as output:
            output.write(txtData) 
        output.close()  
    except:
        print("ERROR SAVING FILE: " + fileName)