import re
import json
import pickle
#import word2vec
from scipy import spatial

def getWords(data):
    return re.compile(r"[\w']+").findall(data)

def uniquefy(a):
    b=[]
    for i in a:
        if i not in b:
            b.append(i)
    return b

with open('../data/output_pos.txt', 'r') as myfile:
    data=myfile.read().replace('\n', '')
a=getWords(data)
#print "\n",a,"\n"
b=[] # b has all the tagger output
for i in range(len(a)):
    b.append(a[i].split('_'))
print b
q=[] #q has dependencies

with open('../data/output_dep.txt','r') as myfile2:
    p=myfile2.readlines()
for i in range(len(p)):
    if p[i][0] != ' ' and p[i][0] != '(' and p[i] != '\n':
        q.append(re.findall(r"[\w':]+", p[i]))
#print len(p), len(q)

print "\n",q,"\n"
#pre processing
allvb=[]
vbdump=[]
allnn=[]
nndump=[]
allother=[]
otherdump=[]
for i in range(len(b)):
    #print i
    #print b[i]
    if b[i][1] == "NN" or b[i][1] == "NNP" or b[i][1] == "NNS"  or b[i][1] == "NNPS":
        if b[i][0] not in nndump:
            nndump.append(b[i][0])
            allnn.append(b[i][0])
    if b[i][1] == "VBN" or b[i][1] == "VBZ" or b[i][1] == "VBG" or b[i][1] == "VB" or b[i][1] == "VBD" or b[i][1] == "VBP":
        if b[i][0] not in vbdump:
            vbdump.append(b[i][0])
            allvb.append(b[i][0])
    if b[i][1] != "NN" and b[i][1] != "NNP":
        if b[i][0] not in otherdump:
            otherdump.append(b[i][0])
            allother.append(b[i][0])
#print allvb
#print allnn
#print " "
dlist=['nsubj','compound', 'nmod:of', 'nmod', 'nmod:to', 'nmod:in', 'nmod:poss', 'amod', 'advmod', 'dep']
nlist=['neg']
q_neg=[]
for i in range(len(q)):
    if q[i][0] in nlist:
        q_neg.append(q[i])
#print "\n", q_neg,"\n"
ie=[]
#print q
#for i in range(len(q)):
#    if q[i][0] in dlist:
bdump=[]
qsave=[]
for i in range(len(q)):#
    if q[i][0] in dlist:
        if q[i][3] in allnn and q[i][1] not in allnn:
            temp=q[i][1]
            q[i][1]=q[i][3]
            q[i][3]=temp
        j=0
        symbup = "->"
        for j in range(len(q_neg)):
            if q_neg[j][1] == q[i][3]:
                symbup = "-!>"
                break
            else:
                symbup = "->"
            j=j+1
        #print q[i][0], symbup
        if q[i][0] == 'compound':
            symbup = "<->"
        #symbup="->"
        if q[i][0] == 'nmod:of':
            symbup = "of"
        elif q[i][0] == 'nmod:poss':
            symbup = "poss"
        elif q[i][0] == 'nmod:to':
            symbup = "to"
        elif q[i][0] == 'nmod:in':
            symbup = "in"
        elif q[i][0] == 'amod':
            symbup = "mod"
            temp=q[i][1]
            q[i][1]=q[i][3]
            q[i][3]=temp
        elif q[i][0] == 'advmod':
            symbup = "mod"
            temp=q[i][1]
            q[i][1]=q[i][3]
            q[i][3]=temp
        elif q[i][0] == 'dep':
            symbup = "dep"
        ie.append((q[i][1] + "_" + symbup + "_" + q[i][3]).split('_'))

bdump=[]
for i in range(len(allnn)):
    #print allnn[i]
    #print " "
    for j in range(len(q)):
        #print q[j]
        #print " "
        if allnn[i] == q[j][1] and q[j][3] in allvb:
            for k in range(len(q)):
                #print q[k]
                if j!=k and q[j][3] == q[k][3] and q[k][1] in allnn:
                    ie.append((q[j][1] + "_" + q[k][3] + "_"  +  q[k][1]).split('_'))
                if j!=k and q[j][3] == q[k][1] and q[k][3] in allnn:
                    ie.append((q[j][1] + "_" + q[k][1] + "_"  +  q[k][3]).split('_'))
        if allnn[i] == q[j][3] and q[j][1] in allvb:
            for k in range(len(q)):
                #print q[k]
                if j!=k and q[j][1] == q[k][3] and q[k][1] in allnn:
                    ie.append((q[j][3] + "_" + q[k][3] + "_"  + q[k][1]).split('_'))
                if j!=k and q[j][1] == q[k][1] and q[k][3] in allnn:
                    ie.append((q[j][3] + "_" + q[k][1] + "_"  +  q[k][3]).split('_'))

ie=uniquefy(ie)
#print " "
#print ie
#print " "
newvb=[]
for i in range(len(ie)):
    if ie[i][1] not in newvb:
        newvb.append(ie[i][1])
#print "\n ``````````````"
#print allvb
#print "\n   ````````````", newvb
json.dump(ie, open("./knowledge/data/triplet.txt",'w'))

diagra = "#!/bin/sh\n#!/bin/bash\n\necho \"digraph G { "

for i in ie:
    if i[1] == "->":
        temp = "dc"
    elif i[1] == "-!>":
        temp = "idc"
    elif i[1] == "<->":
        temp = "co"
    else:
        temp = i[1]

    diagra = diagra + " " + i[0] + "->" + i[2] + " [ label=\"" + temp + "\" ]" + ";"
diagra = diagra + " }\" | dot -Tpng > ./knowledge/data/ie.png"

#print diagra
kg = open("./knowledge/kg.sh",'w')
kg.write(diagra)
kg.close()
