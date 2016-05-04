import numpy as np
import fastdot
import os
from operator import itemgetter


papers = []
citation = []
idHash = dict()

# number of papers
numPaper = 0

# loading paper id and names
# papers = [ ['paperid0', 'papername0'], 
#            ['paperid1', 'papername1'],
#            ... ...
#          ]
#
# idHash[ 'paperid#' ] = paperid0's index in papers
# e.g. idHash[ 'paperid0' ] = 0

count = 0
f = open("pub_out_paper_id.txt", 'r')
for line in f: 
    items = line.split("\t")
    papers.append([items[0], items[1].rstrip('\r\n')])
    idHash[items[0]] = count
    count += 1

numPaper = len(papers)

# loading paper citation relations
# citation = [ ['paperid0', 'paperid0's citationid0', 'paperid0's citationid1' ... ], 
#              ['paperid1', 'paperid1's citationid0', 'paperid1's citationid1' ... ],
#               ... ...
#            ]

citationCount2ndOrder = np.zeros(numPaper)

count = -1
f = open("pub_out_paperid_citpaper.txt", 'r')
for line in f:
    items = line.split("\t")
    if len(citation)!=0 and items[0] == citation[len(citation)-1][0]:
        citation[len(citation)-1].append(items[1].rstrip('\r\n'))
    else:
        citation.append([items[0], items[1].rstrip('\r\n')])
        count += 1
    citationCount2ndOrder[count] += 1

# W_first and W_second are adjacency matrices, both #papers by # papers
# W_first[i][j] = 1 if the ith paper is cited or cites the jth paper
# W_second[i][j] = 1 if the ith paper and jth paper has citation connection to at least one kth paper

W_first = np.zeros((numPaper, numPaper))
W_second = np.zeros((numPaper, numPaper))

for item in citation:
    for i in range(1,len(item)):
        if idHash.has_key(item[0]) and idHash.has_key(item[i]):
            W_first[idHash[item[0]],idHash[item[i]]] += 1

if os.path.exists("W_second.npy"):
    W_second = np.load('W_second.npy')
else:
    # calculate number of paths between two papers on second order
    # then set to 1 if there is at least one path 
    # np.dot(W_first, W_first_T, W_second)
    W_first_T = W_first.transpose()
    W_second = fastdot.dot(W_first, W_first_T)  #np.dot
    np.fill_diagonal(W_second, 0.0)
    np.save('W_second.npy', W_second)

# calculate W_second till this line

if os.path.exists("W_third.npy"):
    W_second = np.load('W_third.npy')
else:
    # calculate number of paths between two papers on second order
    # then set to 1 if there is at least one path 
    # np.dot(W_first, W_first_T, W_second)
    W_second_T = W_second.transpose()
    W_third = fastdot.dot(W_second, W_second_T) #np.dot
    np.fill_diagonal(W_third, 0.0)
    np.save('W_third.npy', W_second)




# calculate number of paths between two papers on third order, commented out to reduce calculation
# thirdOrder = np.dot(secondOrder, secondOrder.transpose())

# simularity calculation (1st order)
# for testing purposes, we chood to calculate simularity for the 4th paper, i.e. paper[3]
# note that some papers, for example, paper[0], it doesn't have any 1st order connections due to the sparsity of our citation network
# paper[0] has citations, but are not listed in our set of papers
queryIndex = idHash['473736']
paperUnion = []
for i in range(numPaper):
    paperUnion.append( citationCount2ndOrder[queryIndex] + citationCount2ndOrder[i] - W_first[queryIndex][i])

similarity2ndOrder = W_first[queryIndex]/paperUnion

#TODO: rank similarity1stOrder

#2nd order citation count, if A cites B which cites C, then A has one 2nd order citation count
paperUnion = []
for i in range(numPaper):
    paperUnion.append( citationCount2ndOrder[queryIndex] + citationCount2ndOrder[i] - W_second[queryIndex][i])

similarity2nOrder = W_second[queryIndex]/paperUnion


# citationCount3rdOrder = np.dot(W_first, citationCount1stOrder) - citationCount1stOrder

PaperScores = []
for i in range(numPaper):
    PaperScores.append((similarity2ndOrder[i],i))

sortedPaperScores = sorted(PaperScores, key = itemgetter(0), reverse = True)
print "Sorted paper scores for paper: " + papers[queryIndex][1]
for i in range(10):
    print str(i+1)+"th similar paper: "+papers[sortedPaperScores[i][1]][1].rstrip('\n')+" with score: "+str(sortedPaperScores[i][0])





