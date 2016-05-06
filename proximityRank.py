import numpy as np
import fastdot
import os
from operator import itemgetter

from calculateProximityRankScore import calculateProximityRankScore

papers = []
authorToPaper = dict()
paperToAuthor = dict()
citation = []
idHash = dict()

# number of papers
numPaper = 0

# loading author paper relationship
count = 0
f = open("pub_out_paperid_author.txt", 'r')
for line in f: 
    items = line.split("\t")
    authorName = items[1].rstrip('\r\n')
    paperToAuthor[count] = authorName
    if not authorToPaper.has_key(authorName):
        authorToPaper[authorName] = []
    authorToPaper[authorName].append(items[0])
    count += 1

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

citationCount1stOrder = np.zeros(numPaper)
citationCount2ndOrder = np.zeros(numPaper)

f = open("pub_out_paperid_citpaper.txt", 'r')
for line in f:
    items = line.split("\t")
    if len(citation)!=0 and items[0] == citation[len(citation)-1][0]:
        citation[len(citation)-1].append(items[1].rstrip('\r\n'))
    else:
        citation.append([items[0], items[1].rstrip('\r\n')])


# W_first and W_second are adjacency matrices, both #papers by # papers
# W_first[i][j] = 1 if the ith paper is cited or cites the jth paper
# W_second[i][j] = 1 if the ith paper and jth paper has citation connection to at least one kth paper

W_first = np.zeros((numPaper, numPaper))
W_second = np.zeros((numPaper, numPaper))
W_third = np.zeros((numPaper, numPaper))

for item in citation:
    for i in range(1,len(item)):
        if idHash.has_key(item[0]) and idHash.has_key(item[i]):
            W_first[idHash[item[0]],idHash[item[i]]] += 1
    if idHash.has_key(item[0]):        
        citationCount1stOrder[idHash[item[0]]] = len(item) - 1


citationCount2ndOrder = np.dot(W_first, citationCount1stOrder) - citationCount1stOrder

# second order adjacency matrix

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

# third order adjacency matrix

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




# query for author similarity


queryAuthor = "Christos Faloutsos"
# queryAuthor = "Jiawei Han"


# simularity calculation 

authorCount = dict()

for paper in authorToPaper[queryAuthor]:
    paperScore = calculateProximityRankScore (idHash[paper], W_first, W_second, W_third, citationCount1stOrder,citationCount2ndOrder)
    sortedPaperScore = sorted(paperScore, key = itemgetter(0), reverse = True)
    for score in sortedPaperScore:
        scoreValue = score[0]
        if np.isnan(scoreValue) or np.isinf(scoreValue):
            scoreValue = 0
        if authorCount.has_key(paperToAuthor[score[1]]):
            authorCount[paperToAuthor[score[1]]] += scoreValue
        else:
            authorCount[paperToAuthor[score[1]]] = scoreValue

authorScore = []
for key, value in authorCount.iteritems():
    authorScore.append((value, key))

sortedAuthorScore = sorted(authorScore, key = itemgetter(0), reverse = True)

print "Sorted author scores for author: " + queryAuthor
for i in range(10):
    print str(i+1)+"th similar author: "+ sortedAuthorScore[i][1] +" with score: "+str(sortedAuthorScore[i][0])




