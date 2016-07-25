import time

'''
millis1 = int(round(time.time() * 1000))
#MALT

from nltk.parse import malt
mp = malt.MaltParser('../lib/maltparser-1.9.0', '../lib/engmalt.linear-1.7.mco')
print mp.parse_one('I shot an elephant in my pajamas .'.split()).tree()

millis2 = int(round(time.time() * 1000))
print millis2-millis1'''
millis2 = int(round(time.time() * 1000))
#STANFORD

from nltk.parse.stanford import StanfordDependencyParser
path_to_jar = '../lib/stanford-parser/stanford-parser.jar'
path_to_models_jar = '../lib/stanford-parser/stanford-parser-3.6.0-models.jar'
dependency_parser = StanfordDependencyParser(path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar)

result = dependency_parser.raw_parse('I shot an elephant in my sleep')
dep = result.next()
a = list(dep.triples())

print a
print a[0]
print a[0][0]
print a[0][0][0]

millis3 = int(round(time.time() * 1000))
print millis3-millis2



millis4 = int(round(time.time() * 1000))
print millis4-millis3
