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

def writeCompleteDictDataToCSV(filename, dict):
    csv_columns = getAllFeatures(dict)
    csv_columns.append('CARAVAN')
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

def getCategoriesT(feature, data):
    cat_dict = {}
    for id in range(len(data)):
        current = int(data[id][feature])


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
    beta = categories[1] - categories[0]
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

# Get a smoothed epsilon by using a Laplace Estimator with alpha = 1, beta = |C|
def getSmoothedEpsilon(feature, category, data, beta):
    n = len(data)
    nx = getNX(feature, category, data) + beta
    nc = getNX('CARAVAN', 1, data)
    ncx = getNCX(feature, category, 'CARAVAN', 1, data) + 1
    pc = nc / float(n)
    pcx = ncx / float(nx)
    epsilon = nx * (pcx - pc) / math.sqrt(nx * pc * (1 - pc))
    return epsilon

def getScoresFromFeatures(feature_list, training_data, test_data, all_data, smoothing):
    scores = getAllScoresFromFeatures(training_data, all_data, smoothing)
    id_scores = {}
    new_data = []
    for id in range(len(test_data)):
        id_scores = {}
        for feature in test_data[id].keys():
            if feature in feature_list:
                category = int(test_data[id][feature])
                id_scores[feature] = scores[feature][category]
        id_scores['NID'] = test_data[id]['NID']
        id_scores['CARAVAN'] = test_data[id]['CARAVAN']
        new_data.append(id_scores)
    return new_data

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

def getAllScores(training_data, test_data, all_data, smoothing):
    scores = getAllScoresFromFeatures(training_data, all_data, smoothing)
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

def getAllScoresFromFeatures(training_data, all_data, smoothing):
    features = getFeatures(training_data)
    scores = {}
    for feature in features:
        scores[feature] = getScoresFromFeature(feature, training_data, all_data, smoothing)
    return scores

def getScoresFromFeature(feature, training_data, all_data, smoothing):
    categories = getCategories(feature, all_data)
    beta = categories[1] - categories[0]
    scores = {}
    if smoothing == 0:
        for category in range(categories[0], categories[1] + 1):
            scores[category] = getScore(feature, category, training_data)
    elif smoothing == 1:
        for category in range(categories[0], categories[1] + 1):
            scores[category] = getSmoothedScore(feature, category, training_data, beta)
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

def getSmoothedScore(feature, category, data, beta):
    n = len(data)
    nx = getNX(feature, category, data)
    nc = getNX('CARAVAN', 1, data)
    ncx = getNCX(feature, category, 'CARAVAN', 1, data)
    pxc = (ncx + 1) / (float(nc) + beta)
    pxnc = (nx - ncx + 1) / float(n - nc + beta)
    score = math.log(pxc/pxnc)
    return score

training_data = readDataFromCSV('tic_training.csv')
test_data = readDataFromCSV('tic_test.csv')
all_data = readDataFromCSV('all_data.csv')

fl = ["PPERSAUT", "PBRAND", "APLEZIER", "MKOOPKLA", "MOSTYPE", "MOSHOOFD",
"APERSAUT", "PWAPART", "AWAPART", "ABYSTAND", "MHHUUR", "MHKOOP", "PPLEZIER"]
scores_nsm = getScoresFromFeatures(fl, training_data, training_data, all_data, 0)
scores_sm = getScoresFromFeatures(fl, training_data, training_data, all_data, 1)
writeCompleteDictDataToCSV('scores_trainingset_15F_nsm.csv', scores_nsm)
writeCompleteDictDataToCSV('scores_trainingset_15F_sm.csv', scores_sm)
scores_nsm = getScoresFromFeatures(fl, training_data, test_data, all_data, 0)
scores_sm = getScoresFromFeatures(fl, training_data, test_data, all_data, 1)
writeCompleteDictDataToCSV('scores_testset_15F_nsm.csv', scores_nsm)
writeCompleteDictDataToCSV('scores_testset_15F_sm.csv', scores_sm)
