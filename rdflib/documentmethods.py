""" DocumentMethods
This module handles all document related operations; adding, editing or deleting a document
"""

##########################################################
## 
## Imports
##
##########################################################

import globals

##########################################################
## 
## Globals
##
##########################################################

edocol = globals.edocol
edodoc = globals.edodoc
Literal = globals.Literal

##########################################################
## 
## Functions
##
##########################################################

def new(pid, name, content):
  """ pre:  id,  unique time
      post: a new page id is added to g. The user is added as owner and to the whitelist and a first
      version of the document is created. """
  #Initialisation
  did = globals.newdid()
  
  # Create initial nodes
  globals.g.add((edodoc[str(did)], edodoc['type'], Literal("document")))
  
  # Setting owner, reverse owner and 
  globals.g.add((edodoc[str(did)], edodoc['owner'], edocol[str(pid)]))              # ownership
  
  # Assign values
  globals.g.add((edodoc[str(did)], edodoc['name'], Literal(name) ))             # assign name
  globals.g.add((edodoc[str(did)], edodoc['content'], Literal(content)))             # assign empty content
  #Write database
  globals.writedb()
  return did
  
def edit(did, name, content):
  """ pre: nonempty id, time, contributor 
      post: false if contributor notin whitelist
      a new version of the page, with the updated content/name attached to the document. 
  """
  #Initialisation
  
  # create a new version
  try: oldname = globals.g.query("""                                  
          SELECT ?name
          WHERE {edodoc:?did edodoc:name ?name .}""", 
          initNs=globals.ns, initBindings={'?did': did})                        # Get original name
  except:
    oldname = ""
  
  if (oldname != name):                                                         # Add a new name, if appliable
    globals.g.set((edodoc[str(did)], edodoc['name'], Literal(name)))
      
  globals.g.set((edodoc[str(did)], edodoc['content'], Literal(content)))        # Add the content  

  #Write database
  globals.writedb()
  return did
  
def delete(did):
  """ pre: identifier van een page
      post: de page word verwijdert """
  
  ###################
  ## H4xx0rz
  ##################$
  
  # delete type
  target = globals.g.query( """
                SELECT ?v 
                WHERE { edodoc:%s edodoc:type ?v .}""" % (did, ), 
                initNs=globals.ns).serialize('python')
  print target
  globals.g.remove((edodoc[str(did)], edodoc['type'], target[0]))

  # delete type
  target = globals.g.query( """
                SELECT ?v 
                WHERE { edodoc:%s edodoc:owner ?v .}""" % (did, ), 
                initNs=globals.ns).serialize('python')   
  globals.g.remove((edodoc[str(did)], edodoc['owner'], target[0]))
  
  # delete type
  target = globals.g.query( """
                SELECT ?v 
                WHERE { edodoc:%s edodoc:name ?v .}""" % (did, ), 
                initNs=globals.ns).serialize('python')   
  globals.g.remove((edodoc[str(did)], edodoc['name'], target[0]))
  
  # delete type
  target = globals.g.query( """
                SELECT ?v 
                WHERE { edodoc:%s edodoc:content ?v .}""" % (did, ), 
                initNs=globals.ns).serialize('python')   
  globals.g.remove((edodoc[str(did)], edodoc['content'], target[0]))

    
  #Write database
  globals.writedb()
  return True
  
def get(did):
  """ pre: a valid id
      return: a list containing [name, contents]
  """
  #print "received get request"
  #Get it's name and content
  #try:  

  results = globals.g.query( """
                SELECT ?p ?n
                WHERE { edodoc:%s ?p ?n . }""" % (did, ) , 
                initNs=globals.ns).serialize(format='python')
                  
  assert results <> [], 'Document does not exist'                               # is did an existing document?
  return globals.parse_pyformat_many(results)
  
def getlastxgeneral(number):
  results = []
  id = int(globals.newdid())
  while (len(results) <> number):
    id = id-1
    if id < 0:
      break
    else:
      if (globals.g.query( """
                    SELECT ?p ?n
                    WHERE { edodoc:%s ?p ?n . }""" % (id, ) , 
                    initNs=globals.ns).serialize(format='python') == []):
        pass
      else:
        results = results + [str(id)]      
                  
  assert results <> [], 'No documents at all in this database'
  return results

def get_property_value(did, property):
  """ pre: a valid id
      return: a list containing [name, contents]
  """
  #print "received get request"
  #Get it's name and content
  #try:  

  results = globals.g.query( """
                SELECT ?n
                WHERE { edodoc:%s edodoc:%s ?n .
                      }""" % (did, property,) , 
                initNs=globals.ns).serialize(format='python')
  print results
                  
  assert results <> [], 'Document/Property does not exist'                      # is did an existing document?
  return globals.parse_pyformat_one(results)

def getalluser(pid):
  """ 
  """
  try:
    results = globals.g.query( """
                SELECT ?id
                WHERE { ?id edodoc:owner edocol:%s .
                      }""" % (pid,) , 
                initNs=globals.ns).serialize(format='python')
  except:
    results = []

  output = []  
  if results != []:
    temp = globals.parse_pyformat_one(results)
    #filter only the values
    for i in temp:                                                              # for each result
      p = len(i) -1                                                               # set the last position
      a = i[p:]                                                                   # get the last value from the result
      while (i[p] != "/") and (p>0):                                                          # while we haven't got the whole value
        p = p-1                                                                   # set the boundary lower
        a = i[p:]                                                                 # add that extra character
      if i[p] == "/": 
        output.append(i[p+1:])
      else:
        output.append(i[p:])
  return output