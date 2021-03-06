import numpy as np

def get_label_classes():
    labels_path = 'data/devanagari-character-dataset/labels.csv'
    '''
    This method will import labels.csv from the dataset and retreive the clean label classes
    and return them as a dictionary
    '''
    with open("%s" % (labels_path)) as labels:
        content = [value.replace(",,,", "")
                   for value in labels.read().split("\n") if value != ",,,"]
        clean_data = {}
        clean_data["labels"] = content[1]
        clean_data["numerals"] = content[2:12]
        clean_data["vowels"] = content[14:26]
        clean_data["consonants"] = content[28:64]
        return clean_data

def get_character(number,label_type):
    newlist = get_label_classes()[label_type]
    for row in newlist:
        if int(row.split(",")[0]) == number:
            print(row.split(",")[2])
            return row.split(",")[2]

def get_data(values_path, labels_path):
    '''
    This method will load the npy arrays that are generated by clean.py
    and it will return it in a tuple
    '''
    values = np.load(values_path)
    labels = np.load(labels_path)
    return (values, labels)
