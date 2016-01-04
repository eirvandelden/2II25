import globals
edocol = globals.edocol

def documents(arg):
  pass
  '''
  if arg[0] == 'owner':
    print 'owner'
    # find all docs with property value
    results = globals.g.query( """
                SELECT ?id
                WHERE { ?id edodoc:owner edocol:%s .
                      }""" % (arg[1],) , 
                initNs=globals.ns).serialize(format='python')

    results = globals.g.query("""
                  SELECT ?id ?p ?value 
                  WHERE {?id edocol:owner edocol:%s  . 
                         ?id ?p ?value .}""" % arg[1], 
                  initNs=globals.ns).serialize('python') 

    output = []
    for row in results:
      if (row[1] == arg[0]) and (row[2] == Literal[arg[1]]):
        output = output + [row] 
    print output        
        
  else:
    print 'not owner'
    # find all docs with property value
    results = globals.g.query("""
                  SELECT ?id ?p ?value 
                  WHERE {?id edodoc:%s %s . 
                         ?id ?p ?value .}""" % (arg[0],arg[1]), 
                  initNs=globals.ns).serialize('python') 

    output = []
    for row in results:
      if (row[1] == arg[0]) and (row[2] == Literal[arg[1]]):
        output = output + [row]  
    print output  

  return globals.parse_pyformat_many(globals.individual(output))     '''

# nog te doen?
def users(arg):

  # find all users with property value
  results = globals.g.query("""
                SELECT ?id ?p ?value 
                WHERE {?id edocol:%s edocol:%s  . 
                       ?id ?p ?value .}""" % (arg[0], arg[1]), 
                initNs=globals.ns).serialize('python') 

  output = []
  for row in results:
    if (row[1] == edocol[arg[0]]) and (row[2] == edocol[arg[1]]):
      output = output + [row]   

  return globals.parse_pyformat_many(globals.individual(output)) 