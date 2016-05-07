import numpy as np

def calculateProximityRankScore (queryIndex, W_first, W_second, W_third, citationCount1stOrder,citationCount2ndOrder, secondOrderThreshold, thirdOrderThreshold):
    numPaper = len(citationCount1stOrder)
    #1st order citation count
    similarity1stOrder = W_first[queryIndex]
    #2nd order citation count, if A cites B which cites C, then A has one 2nd order citation count
    paperUnion = []
    for i in range(numPaper):
        paperUnion.append( citationCount1stOrder[queryIndex] + citationCount1stOrder[i] - W_second[queryIndex][i] )

    similarity2ndOrder = np.divide(W_second[queryIndex],paperUnion)
    similarity2ndOrder[similarity2ndOrder > secondOrderThreshold] = 1
    #3rd order citation count
    paperUnion = []
    for i in range(numPaper):
        paperUnion.append( citationCount2ndOrder[queryIndex] + citationCount2ndOrder[i] - W_third[queryIndex][i])
    similarity3rdOrder = np.divide(W_third[queryIndex],paperUnion)
    similarity3rdOrder[similarity3rdOrder > thirdOrderThreshold] = 1


    # ranking combination score
    PaperScores = []
    for i in range(numPaper):
        PaperScores.append((similarity1stOrder[i]/2.0+ (similarity2ndOrder[i]/3.0) + (similarity3rdOrder[i]/6.0),i))


    return PaperScores