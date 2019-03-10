import csv
import math

def getDataFromCSV(filename):
    dict_list = []
    reader = csv.DictReader(open(filename, 'rb'))
    for line in reader:
        dict_list.append(line)
    return dict_list

def getFeatures(data):
    features = []
    for feature in data[0]:
        if feature != 'NID':
            features.append(feature)
    return features

def getCategories(feature, data):
    count = 0
    for id in range(len(data)):
        if int(data[id][feature]) > count:
            count = int(data[id][feature])
    return count

def getNX(feature, category, data):
    count = 0
    for id in range(len(data)):
        if category == int(data[id][feature]):
            count = count + 1
    #fc = str(feature) + ' (Cat: ' + str(category) + ')'
    #print fc + ': ' + str(count)
    return count

def getNCX(feature1, category1, feature2, category2, data):
    count = 0
    for id in range(len(data)):
        if category1 == int(data[id][feature1]) and category2 == int(data[id][feature2]):
            count = count + 1
    #fc1 = str(feature1) + ' (Cat: ' + str(category1) + ')'
    #fc2 = str(feature2) + ' (Cat: ' + str(category2) + ')'
    #print fc1 + ' AND ' + fc2 + ': ' + str(count)
    return count

def getAllEpsilons(data):
    features = getFeatures(data)
    epsilons = {}
    for feature in features:
        epsilons[feature] = getEpsilonsFromFeature(feature, data)
    return epsilons

def getEpsilonsFromFeature(feature, data):
    categories = getCategories(feature, data)
    epsilons = {}
    for category in range(1, categories + 1):
        epsilons[category] = getEpsilon(feature, category, data)
    return epsilons

def getEpsilon(feature, category, data):
    n = len(data)
    nx = getNX(feature, category, data)
    nc = getNX('CARAVAN', 1, data)
    ncx = getNCX(feature, category, 'CARAVAN', 1, data)
    if n != 0 and nx != 0:
        pc = nc / float(n)
        pcx = ncx / float(nx)
        epsilon = nx * (pcx - pc) / math.sqrt(nx * pc * (1 - pc))
    else:
        epsilon = 0
    #print 'Epsilon :' + str(epsilon)
    return epsilon

all_data = getDataFromCSV('tic_training.csv')
features = getFeatures(all_data)
