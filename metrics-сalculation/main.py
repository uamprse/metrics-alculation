# name: russian_demography.csv
# region: Republic of Dagestan  Sevastopol
# id: npg



def readFile(fileName):
    if fileName.endswith('.csv'):
        with open(fileName, 'r') as file:
            if file.read(1) == '':
                raise Exception("Empty file")
            keys = file.readline().strip().split(',')
            return [dict(zip(keys, line.strip().split(','))) for line in file]
    else:
        raise Exception("Invalid file name. Requires .csv extension")

def printRow(row):
    for i in row:
        print('%-22s' % i, end=' ')
    print('\n')
def printKeys(keys):
    for i in keys:
        print('%-22s' % i, end = ' ')
    print('\n')

def sortedMas(region, mas, id):
    data = []
    keys = ' '.join(mas[0].keys()).split(' ')
    printKeys(keys)
    for elem in mas:
        row = ','.join(elem.values())
        if elem["region"] == region:
            if ",," in row:
                raise ValueError("Invalid string. Metric calculation is not possible. Select another region")
            else:
                row = row.split(',')
                printRow(row)
                data.append(float(elem[id]))
    if not data:
        raise ValueError("Get empty list of params")
    return data

def checkRegion(region, data):
    if not region in [elem['region'] for elem in data]:
        raise ValueError("Invalid region")

def checkID(id, data):
    if not id in data[0].keys():
        raise ValueError("Invalid id")

def findMax(data):
    return max(data)

def findMin(data):
    return min(data)

def findMedian(data):
    data.sort()
    number = len(data)
    if number % 2 == 0:
        number = (data[number // 2] + data[number // 2 - 1]) / 2
    else:
        number = data[number // 2]
    return number

def findAverage(data):
    summ = 0
    for elem in data:
        summ += elem
    return summ/(len(data))

def findPercentiles(listParams):
    listParams.sort()
    percentiles = list(range(0, 101, 5))
    percentilesValues = []

    for percentile in percentiles:
        index = int(percentile / 100 * (len(listParams) - 1))
        percentilesValues.append(listParams[index])

    return dict(zip(percentiles, percentilesValues))

def calculateMetrics(data):
    maxElem = findMax(data)
    minElem = findMin(data)
    medianElem = findMedian(data)
    averageElem = findAverage(data)
    newMetric = calculateNewMetric(data, averageElem)
    print(f"max: {maxElem} \nmin: {minElem} \nmedian: {medianElem} \naverage: {averageElem} \nnewMetric: {newMetric}\n")

def calculatePercentiles(data):
    percentiles = findPercentiles(data)
    print('%-10s' % "N%",'%-10s' % "value")
    for key, value in percentiles.items():
        print('%-10s' % key,'%-10s' % value)


def calculateNewMetric(data, averageElem):
    sum = 0
    lenOfData = len(data)
    for i in range(0, lenOfData):
        sum += (data[i] - averageElem)**2
    sum /= lenOfData
    return sum


def readData(fileName):
    mas = readFile(fileName)
    region = input("region: ")
    checkRegion(region, mas)
    id = input("id: ")
    checkID(id, mas)
    data = sortedMas(region, mas, id)
    return data

if __name__ == '__main__':
    fileName = input("name: ")
    try:
        data = readData(fileName)
        calculateMetrics(data)
        calculatePercentiles(data)
    except Exception as e:
        print(e)