import csv
import math

def readDataFromCSV(filename):
    dict_list = []
    reader = csv.DictReader(open(filename, 'rb'))
    for line in reader:
        dict_list.append(line)
    return dict_list

# Write a "Feature - Category - Value" type dictionary to a CSV
def writeFCVDataToCSV(filename, dict):
    with open(filename, 'w') as file:
        for feature in dict.keys():
            for category in dict[feature].keys():
                file.write("%s,%s,%s\n"%(feature, category, dict[feature][category]))

def writeDictDataToCSV(filename, dict):
    csv_columns = getAllFeatures(dict)
    with open(filename, 'w') as file:
        writer = csv.DictWriter(file, fieldnames = csv_columns)
        writer.writeheader()
        for row in dict:
            writer.writerow(row)

def getAllFeatures(data):
    features = []
    for feature in data[0]:
        if feature != 'CARAVAN':
            features.append(feature)
    return features

def getFeatures(data):
    features = []
    for feature in data[0]:
        if feature != 'NID' and feature != 'CARAVAN':
            features.append(feature)
    return features

def getCategories(feature, data):
    mincount = int(data[0][feature])
    maxcount = int(data[0][feature])
    for id in range(len(data)):
        current = int(data[id][feature])
        if current > maxcount:
            maxcount = current
        if current < mincount:
            mincount = current
    return mincount, maxcount


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
    for category in range(categories[0], categories[1] + 1):
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

def getSumOfAllScores(data):
    scores = getAllScoresFromFeatures(data)
    id_scores = []
    for id in range(len(data)):
        total_score = 0
        for feature in data[id].keys():
            if feature != 'NID' and feature != 'CARAVAN':
                category = int(data[id][feature])
                total_score = total_score + scores[feature][category]
        id_scores.append(total_score)
    return id_scores

def getAllScores(training_data, test_data, all_data):
    scores = getAllScoresFromFeatures(training_data, all_data)
    id_scores = {}
    new_data = []
    for id in range(len(test_data)):
        id_scores = {}
        for feature in test_data[id].keys():
            if feature == 'NID':
                id_scores[feature] = test_data[id][feature]
            elif feature != 'CARAVAN':
                category = int(test_data[id][feature])
                id_scores[feature] = scores[feature][category]
        new_data.append(id_scores)
    return new_data

def getAllScoresFromFeatures(training_data, all_data):
    features = getFeatures(training_data)
    scores = {}
    for feature in features:
        scores[feature] = getScoresFromFeature(feature, training_data, all_data)
    return scores

def getScoresFromFeature(feature, training_data, all_data):
    categories = getCategories(feature, all_data)
    scores = {}
    for category in range(categories[0], categories[1] + 1):
        scores[category] = getScore(feature, category, training_data)
    return scores

def getScore(feature, category, data):
    n = len(data)
    nx = getNX(feature, category, data)
    nc = getNX('CARAVAN', 1, data)
    ncx = getNCX(feature, category, 'CARAVAN', 1, data)
    pxc = ncx / float(nc)
    pxnc = (nx - ncx) / float(n - nc)
    if pxc != 0 and pxnc != 0:
        score = math.log(pxc/pxnc)
    else:
        score = 0
    return score

training_data = readDataFromCSV('tic_training.csv')
test_data = readDataFromCSV('tic_test.csv')
all_data = readDataFromCSV('all_data.csv')
