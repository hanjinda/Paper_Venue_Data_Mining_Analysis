import numpy as np
import os
from operator import itemgetter
import Queue as Q

from calculateProximityRankScore import calculateProximityRankScore

# Parameters #
queryAuthor = "Jiawei Han"
secondOrderThreshold = 0.1
thirdOrderThreshold = 0.1
# score = alpha * proximityRankScore + (1-alpha) * pathSimRankScore 
alpha = 0.5

######################################################################
#
#
#
#    Proximity Rank
#
#
#
######################################################################

papers = []
authorToPaper = dict()
paperToAuthor = dict()
citation = []
idHash = dict()

np.seterr(all='ignore')

# number of papers
numPaper = 0

print "STEP1: loading author paper relationship..."

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

print "STEP2: loading paper id and names..."

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

print "STEP3: loading paper citation relations..."


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


print "STEP4: calculating first order adjacency matrix and citation counts..."


for item in citation:
    for i in range(1,len(item)):
        if idHash.has_key(item[0]) and idHash.has_key(item[i]):
            W_first[idHash[item[0]],idHash[item[i]]] += 1
    if idHash.has_key(item[0]):        
        citationCount1stOrder[idHash[item[0]]] = len(item) - 1


citationCount2ndOrder = np.dot(W_first, citationCount1stOrder) - citationCount1stOrder


print "STEP5: calculating/loading second order adjacency matrix..."

# second order adjacency matrix

if os.path.exists("W_second.npy"):
    W_second = np.load('W_second.npy')
else:
    # calculate number of paths between two papers on second order
    # then set to 1 if there is at least one path 
    # np.dot(W_first, W_first_T, W_second)
    W_first_T = W_first.transpose()
    W_second = np.dot(W_first, W_first_T)  #np.dot
    np.fill_diagonal(W_second, 0.0)
    np.save('W_second.npy', W_second)


print "STEP6: calculating/loading third order adjacency matrix..."

# third order adjacency matrix

if os.path.exists("W_third.npy"):
    W_third = np.load('W_third.npy')
else:
    # calculate number of paths between two papers on second order
    # then set to 1 if there is at least one path 
    # np.dot(W_first, W_first_T, W_second)
    W_second_T = W_second.transpose()
    W_third = np.dot(W_second, W_second_T) #np.dot
    np.fill_diagonal(W_third, 0.0)
    np.save('W_third.npy', W_third)


print "STEP7: calculating proximity ranking ..."


# simularity calculation 

authorCount = dict()

for paper in authorToPaper[queryAuthor]:
    paperScore = calculateProximityRankScore (idHash[paper], W_first, W_second, W_third, citationCount1stOrder,citationCount2ndOrder, secondOrderThreshold, thirdOrderThreshold)
    sortedPaperScore = sorted(paperScore, key = itemgetter(0), reverse = True)
    for score in sortedPaperScore:
        scoreValue = score[0]
        if np.isnan(scoreValue) or np.isinf(scoreValue):
            scoreValue = 0
        if authorCount.has_key(paperToAuthor[score[1]]):
            authorCount[paperToAuthor[score[1]]] += scoreValue
        else:
            authorCount[paperToAuthor[score[1]]] = scoreValue

proximityAuthorScore = []
for key, value in authorCount.iteritems():
    proximityAuthorScore.append((value, key))

proximitySortedAuthorScore = sorted(proximityAuthorScore, key = itemgetter(0), reverse = True)
print "===================================================="

print "Proximity ranking scores for author: " + queryAuthor
print "===================================================="

for i in range(10):
    print str(i+1)+"th similar author: "+ proximitySortedAuthorScore[i][1] +" with score: "+str(proximitySortedAuthorScore[i][0])


######################################################################
#
#
#
#    Path Sim Rank
#
#
#
######################################################################

print "STEP8: loading authors and author ids ..."

authors = dict()
indexToAuthors = dict()

count = 0
f = open("pub_out_authers.txt", 'r')
for line in f: 
    authors[line.rstrip('\r\n')] = count
    indexToAuthors[count] = line.rstrip('\r\n')
    count += 1

print "STEP9: calculating author paper adjacency matrix ..."


W_ap = np.zeros((len(authorToPaper), numPaper))
for author in authors:
    for paper in authorToPaper[author]:
        W_ap[authors[author]][idHash[paper]] = 1

print "STEP10: calculating venue paper adjacency matrix ..."

W_pv = np.zeros((numPaper, 20))
prevVenue = ""
count = -1
f = open("pub_out_paperid_venues.txt", 'r')
for line in f: 
    items = line.split("\t")
    venue = item[1].rstrip('\r\n')
    if venue != prevVenue:
        count += 1
        prevVenue = venue
    W_pv[idHash[items[0]]][count] = 1



W_pa = W_ap.transpose()
W_vp = W_pv.transpose()
print "STEP11: calculating M matrix ..."


if os.path.exists("M.npy"):
    M = np.load('M.npy')
else:
    M = np.dot(np.dot(np.dot(W_ap,W_pv), W_vp),W_pa)
    np.save('M.npy', M)


print "STEP12: calculating pathsim ranking ..."

q_author_index = authors[queryAuthor]

# sort rankings 
pathSimAuthorScores = []

for i in range(len(authors)):
    score = 2*M[q_author_index][i]/(M[q_author_index][q_author_index] + M[i][i])
    pathSimAuthorScores.append((score,i))

pathSimSortedAuthorScores = sorted(pathSimAuthorScores, key = itemgetter(0), reverse = True)
print "===================================================="

print "PathSim ranking scores for author: " + queryAuthor
print "===================================================="

for i in range(10):
    print str(i+1)+"th similar author: "+ indexToAuthors[pathSimSortedAuthorScores[i][1]]+" with score: "+str(pathSimSortedAuthorScores[i][0])

print "STEP13: calculating combined score ..."

proximityScoreMax = proximitySortedAuthorScore[0][0]
pathScoreMax = pathSimSortedAuthorScores[0][0]

scoreSum = np.zeros(len(authors))

# hahaha = 1

for score in proximitySortedAuthorScore:
    scoreSum[authors[score[1]]] += alpha * score[0]/proximityScoreMax
    # if hahaha <= 10:
    #     print "auth score: "+str(authors[score[1]])
    #     print "prox: "+str(alpha * score[0]/proximityScoreMax)
    #     hahaha += 1

hahaha = 1

for score in pathSimSortedAuthorScores:
    scoreSum[score[1]] += (1-alpha) * score[0]/pathScoreMax
    # if hahaha <= 10:
    #     print "score: "+str(score[1])
    #     print "path: "+str(alpha * score[0]/pathScoreMax)
    #     hahaha += 1

# print pathScoreMax
# print "hanhanhan: "+str(scoreSum[57])

combinedScores = []

for i in range(len(authors)):
    combinedScores.append((scoreSum[i], i))

sortedcombinedScores = sorted(combinedScores, key = itemgetter(0), reverse = True)

print "===================================================="
print "Combined ranking scores for author: " + queryAuthor
print "===================================================="


for i in range(10):
    print str(i+1)+"th similar author: "+ indexToAuthors[sortedcombinedScores[i][1]] +" with score: "+str(sortedcombinedScores[i][0])


