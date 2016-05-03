# implementation for the PathSim method
import numpy as np
import Queue as Q
from operator import itemgetter
import argparse


parser = argparse.ArgumentParser()

parser.add_argument('-q', '--query_author', type=str)
parser.add_argument('-p', '--meta_path', type=str)
args = parser.parse_args()


fileList = ["paper.txt", "venue.txt", "author.txt", "term.txt", "relation.txt"]
filePath = "Data/dblp_4area/"
# nodeList items: 0-paper; 1-venue; 2-author; 3-term
nodeList = []
relation = []
idHash = dict()

# parsing files into arrays and ids into dictionary
count = 0

for i in range(4):
    f = open(filePath+fileList[i], 'r')
    nodeType = []
    for line in f: 
        items = line.split("\t")
        nodeType.append([items[0], items[1]])
        idHash[items[0]] = count
        count += 1
    nodeList.append(nodeType)

# construct adjacency matrices, all in respect to paper
W_pvat = np.zeros((len(nodeList[0]), len(nodeList[1])+len(nodeList[2]) + len(nodeList[3])))

f = open(filePath+"relation.txt", 'r')
for line in f:
    items = line.split("\t")
    if len(relation)!=0 and items[0] == relation[len(relation)-1][0]:
        relation[len(relation)-1].append(items[1])
    else:
        relation.append([items[0], items[1]])

paperIndexOffset = len(nodeList[0])
for item in relation:
    for i in range(1,len(item)):
        W_pvat[idHash[item[0]],idHash[item[i]] - paperIndexOffset ] += 1

# adjacency matrices are calculated, W_pv stands for paper-venue
W_pv = W_pvat[:,0:len(nodeList[1])]
W_pa = W_pvat[:,len(nodeList[1]):len(nodeList[1]) + len(nodeList[2])]
W_pt = W_pvat[:,len(nodeList[1]) + len(nodeList[2]):]

W_vp = W_pv.transpose()
W_ap = W_pa.transpose()
W_tp = W_pt.transpose()

# calculate commuting matrix for metapath APVPA
if args.meta_path == "APVPA":
    M = np.dot(np.dot(np.dot(W_ap,W_pv), W_vp),W_pa)
elif args.meta_path == "APTPA":
    M = np.dot(np.dot(np.dot(W_ap,W_pt), W_tp),W_pa)
elif args.meta_path == "APA":
    M = np.dot(W_ap, W_pa)

# calculate rankings
q_author_id = ""
for i in range(len(nodeList[2])):
    if (args.query_author+"\n") == nodeList[2][i][1]:
        q_author_id = nodeList[2][i][0]

if q_author_id == "":
    print "Author not found"
else:
    q_author_index = idHash[q_author_id] - len(nodeList[0]) - len(nodeList[1])

# sort rankings 
AuthorScores = []

for i in range(len(nodeList[2])):
    score = 2*M[q_author_index][i]/(M[q_author_index][q_author_index] + M[i][i])
    AuthorScores.append((score,i))

sortedAuthorScores = sorted(AuthorScores, key = itemgetter(0), reverse = True)

for i in range(10):
    print str(i+1)+"th similar author: "+nodeList[2][sortedAuthorScores[i][1]][1].rstrip('\n')+" with score: "+str(sortedAuthorScores[i][0])









