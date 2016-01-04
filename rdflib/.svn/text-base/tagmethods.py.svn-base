import globals
import re 

edocol = globals.edocol
Literal = globals.Literal

# voeg een nieuwe tag toe
# eigenlijk niet nodig..
def add(tag):

  assert re.match("^[a-zA-Z]+$", tag), 'invalid tag: tag does not consist of only letters'
  
  assert get(tag) == [], 'tag already exists'
  
  globals.g.add( (edocol[tag], edocol["type"], edocol['tag']) )   # add the tag

  #Write database
  globals.writedb()
  return tag
  
def tag(tag, documentid): 
  
  assert re.match("^[a-zA-Z]+$", tag), 'invalid tag: tag does not consist of only letters'
  
  globals.g.add( (edocol[documentid], edocol["tagged"], edocol[tag]) )   # tag the document

  #Write database
  globals.writedb()
  return True

def remove(tag, documentid):
  
  globals.g.remove( (edocol[documentid], edocol["tagged"], edocol[tag]) )   # remove the tag

  #Write database
  globals.writedb()
  return True

def follow(id, tag):

  assert not (get(tag) == []), 'no such tag'
  
  # add new user
  globals.g.add( (edocol[id], edocol["followstag"], edocol[tag]) )   # follow the tag

  #Write database
  globals.writedb()
  return True
  
def delete(tag):
  
  # find all triples about tag
  targets = globals.g.query( """
                SELECT ?s ?p ?v 
                WHERE { edocol:%s ?p ?v .
                        ?s ?p ?v .}""" % tag, 
                initNs=globals.ns).serialize('python')  
                
  targets = targets + globals.g.query( """
                SELECT ?s ?p ?v
                WHERE { ?s ?p edocol:%s .
                        ?s ?p ?v .}""" % tag,
                initNs=globals.ns).serialize('python')  

  # delete everything
  for row in targets:
    if (row[0] == edocol[tag]) or (row[2] == edocol[tag]):
      globals.g.remove(row)
      print row

  #Write database
  globals.writedb()
  return globals.parse_pyformat_many(globals.individual(targets))
  
def get(tag):
  
  # find all triples about tag
  targets = globals.g.query( """
                SELECT ?s ?p ?v 
                WHERE { edocol:%s ?p ?v .
                        ?s ?p ?v .}""" % tag, 
                initNs=globals.ns).serialize('python')  
                
  targets = targets + globals.g.query( """
                SELECT ?s ?p ?v
                WHERE { ?s ?p edocol:%s .
                        ?s ?p ?v .}""" % tag, 
                initNs=globals.ns).serialize('python')  
  
  # get everything
  results = []
  for row in targets:
    if (row[0] == edocol[tag]) or (row[2] == edocol[tag]):
      results = results + [row]

  #Write database
  globals.writedb()
  return globals.parse_pyformat_many(globals.individual(results))
