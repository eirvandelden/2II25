##########################################################
## 
## MODULE: Globals
## Here are functions and variables needed across modules
##
##########################################################

import rdflib
from rdflib import ConjunctiveGraph as Graph
from rdflib import Namespace, Literal
import sha,re,os


##########################################################
## 
## RDF Storage to/from SQLite
##
##########################################################

# Read g from the database
#store = rdflib.plugin.get('SQLite', rdflib.store.Store)('database.ts')# Use SQLite3 to read database.ts
#try:                                                               # try opening the database
#    store.open('', create=True)                                    # create a new database
#except:
#store.open('', create=False)                                        # open an existing database
#g = Graph(store)                                                    # assign database to g
g = Graph()    
g.parse("database.nt", format="nt")
##########################################################
## 
## Namespaces
##
##########################################################

edocol = Namespace("http://edocol.com/namespace/1.0/")
edodoc = Namespace("http://edocol.com/documents/1.0/")

ns = dict(edocol=edocol, edodoc=edodoc)

##########################################################
## 
## Functions
##
##########################################################

def newdid():
  """ pre: true
      post: return int, such that int > \forall id \in \PageID's """
  query = g.query("""
                SELECT ?id 
                WHERE {?id edodoc:type "document" . }""", 
                initNs=ns).serialize(format="python")
  
  return getnewid(query)


# haalt het ID dat we willen hebben uit de resultaten van de query. werkt evt. ook met pageIDs en zo.
def getnewid(results):
  if results == []:
    print 'results == []'
    return '0'
  else:
    longest = 0
    # sorting (see below) is in dictionary style (blaat/0, blaat/1, blaat/10, blaat/2, blaat/3, ..)
    # so we look at the longest entries only.
    for r in results:
      if len(r) > longest:
        longest = len(r)    
    longestresults = []
    for r in results:
      if len(r) == longest:
        longestresults = longestresults + [r]
        
    # sort and get the URI with the highest number    
    longestresults.sort()
    var = longestresults.pop()
    
    # get the number
    for i in range(len(var)-1, 0, -1):
      if var[i] == '/':
        break
    result = str(int(var[i+1:len(var)])+1)
  
    return result

 
# haalt de dubbele voorkomens uit een array.
def individual(results):
  indiv = []
  for n in range(len(results)):
    add = True
    for m in range(n):
      if results[n] == results[m]:
        add = False
    if add == True:
      indiv = indiv + [results[n]]  
      
  return indiv

# voor het parsen van 1 waarde.
def parse_pyformat_one(results):
  output = []
  for word in results:
    output = output + ['']
    read = False
    
    # is dit een URI, zo ja, waar begint de waarde?
    start = 0
    slash = False
    for i in range(len(word)-1, 0, -1):
      if word[i] == '/':
        start = i
        slash = True
        break
    # als URI    
    if slash:   
      at = 0
      for char in word:
        if at > start:
          output[len(output)-1] = output[len(output)-1] + str(char)
        at = at + 1  
    # als niet URI    
    else: 
      for char in word:
        output[len(output)-1] = output[len(output)-1] + char  
    output[len(output)-1] = str(output[len(output)-1])
    
     
  return output
  
# voor het parsen van tuples en triples.  
# Werkt, maar is nog niet helemaal veilig: vertoont onvoorspelbaar gedrag bij waardes met forward slashes erin, 
# bijv. als mensen hun website in de graph kunnen zetten geeft 'http://edocol.com/namespace/1.0/http://homepage.net/' niks terug. 
# (want de functie pakt aleen alles na de slash)
def parse_pyformat_many(results):
  output = []
  for set in results:
    output = output + [[]]
    read = False
    for word in set:
      output[len(output)-1] = output[len(output)-1] + ['']   
      
      if word == None:
        pass
      else:
        # is dit een URI, zo ja, waar begint de waarde?
        start = 0
        slash = False
        for i in range(len(word)-1, 0, -1):
          if word[i] == '/':
            start = i
            slash = True
            break
         
        # als dit een URI is: 
        if slash: 
          at = 0
          for char in word:
            if at > start:
              output[len(output)-1][len(output[len(output)-1])-1] = output[len(output)-1][len(output[len(output)-1])-1] + str(char)
            at = at + 1
        # als dit geen URI is:
        else:
          for char in word:
            output[len(output)-1][len(output[len(output)-1])-1] = output[len(output)-1][len(output[len(output)-1])-1] + str(char)    
  
  return output
# haalt de dubbele voorkomens uit een array.
def individual(results):
  indiv = []
  for n in range(len(results)):
    add = True
    for m in range(n):
      if results[n] == results[m]:
        add = False
    if add == True:
      indiv = indiv + [results[n]]  
      
  return indiv
  
def writedb():
  with open("database.nt", 'w') as output:
      print >>output, g.serialize(format="nt")

if __name__== '__main__':
  print "Hello World!"