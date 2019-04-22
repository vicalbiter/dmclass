def transformWType(datafile, jsonfile):
    catfile = open(jsonfile)
    categories = json.load(catfile)
    data = pd.read_csv(datafile)
    dictionary = {}
    for catname in categories.keys():
        new_column = []
        for element in data.loc[:, catname]:
            new_category = categorizeWType(element, categories[catname])
            new_column.append(new_category)
        dictionary[catname] = new_column
    return pd.DataFrame.from_dict(dictionary, orient="columns")

def categorizeWType(element, categories):
    for key in categories.keys():
        if key != "else" and key != "type":
            if categories["type"] == "cont":
                if str(element) >= categories[key][0] and str(element) < categories[key][1]:
                    return key
            elif categories["type"] == "disc":
                if str(element) in categories[key]:
                    return key
    return categories["else"]

dic1 = transformWType("auto_salud.csv", "catautocont.txt")
dic1.to_csv('pes.csv')

def transform(datafile, jsonfile):
    catfile = open(jsonfile)
    categories = json.load(catfile)
    data = pd.read_csv(datafile)
    dictionary = {}
    for catname in categories.keys():
        new_column = []
        for element in nut.loc[:, catname]:
            new_category = categorize(element, categories[catname])
            new_column.append(new_category)
        dictionary[catname] = new_column
    return pd.DataFrame.from_dict(dictionary, orient="columns")

def categorize(element, categories):
    for key in categories.keys():
        if key != "else":
            if str(element) in categories[key]:
                return key
    return categories["else"]
            
dic = transform('nnutrition.csv', 'catnutrition.txt')
dic
