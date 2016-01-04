##########################################################
## 
## RDF query
##
##########################################################

results = g.query("""
            SELECT ?film ?year 
            WHERE { ?film fb:film.film.initial_release_date ?year. }
            """, initNs={'fb':FBNAMESPACE})
for triple in results: print triple

##########################################################
## 
## SQLite
##
##########################################################

import rdflib      
import sha,re,os

store = rdflib.plugin.get('SQLite', rdflib.store.Store)('<filenaam>') #gebruik sqlite
store.open('<pad naar containing directory>', create=False) #Als de database-file nog niet bestaat, create=True

g = rdflib.ConjunctiveGraph(store)                                  # bind g aan de database  

# Wil je tussendoor checken of alles goed is?
g.serialize(format='nt')

### Afsluiten
g.commit() #schrijf naar disk

Poging tot nieuwe getnewid:
def getnewid(input):
  #initialisation
  index = []
  print "De input is:"
  print input

  #Check for an empty list
  if input == []:
    output = "0"
  else: #input is a list of possible id's
    #filter only the values
    for i in input:                                                              # for each input
      p = len(i)-1                                                               # set the last position
      a = i[p:]                                                                  # get the last value from the result
      #print a
      #start adding characters from back to front until we find a /
      while a[0] != "/":                                                        # while we haven't got the whole value
        p = p-1                                                                 # set the boundary lower
        a = i[p:]                                                               # add that extra character
      #  print "A is: ", a
      #We now have the complete value
      p=p+1
      index.append(i[p:])
      #print "Just added:", i[p:]
      
    # Sort the new array
    sorted(index)
    output = str(int(index.pop())+1)
  return output
