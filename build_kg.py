import re
import json
import pickle
import subprocess
import time
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

def get_b_q(keys):
    b=[]
    q=[]
    for i in keys:
        #print i
        b.append([str(i[0][0]), str(i[0][1])])
        b.append([str(i[2][0]), str(i[2][1])])
        q.append([str(i[1]), str(i[0][0]), str(i[0][1]), str(i[2][0]), str(i[2][1])])
    b = uniquefy(b)
    return b, q

def make_graph(b, q):
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
    json.dump(ie, open("./triplet.txt",'w'))

    diagra = "#!/bin/sh\n#!/bin/bash\n\necho \"digraph G { "
    diagra = "echo \"digraph G { "

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
    diagra = diagra + " }\" | dot -Tpng > ./ie.png"

    #print diagra
    #kg = open("./kg.sh",'w')
    #kg.write(diagra)
    #kg.close()
    print diagra.split()

    subprocess.call(diagra, shell=True)

def lambda_function(event, context):
    #STANFORD

    from nltk.parse.stanford import StanfordDependencyParser
    path_to_jar = '../lib/stanford-parser/stanford-parser.jar'
    path_to_models_jar = '../lib/stanford-parser/stanford-parser-3.6.0-models.jar'
    dependency_parser = StanfordDependencyParser(path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar)

    result = dependency_parser.raw_parse(event)
    dep = result.next()
    a = list(dep.triples())
    #print a
    #print len(a)
    a = get_b_q(a)
    make_graph(a[0], a[1])


millis2 = int(round(time.time() * 1000))

lambda_function("Who does not love a good candy", 0)

millis3 = int(round(time.time() * 1000))
print millis3-millis2
