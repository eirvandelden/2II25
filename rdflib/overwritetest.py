import globals
  
edocol = globals.edocol
Literal = globals.Literal

globals.g.add((edocol['A'], edocol['B'], edocol['C']))
globals.g.add((edocol['D'], edocol['B'], edocol['C']))  

globals.g.set((edocol['A'], edocol['B'], Literal('F')))

print 'D:'
get = globals.g.query("""
            SELECT ?s ?p
            WHERE {?s ?p edocol:C . }""", 
            initNs=globals.ns).serialize('python')
print get