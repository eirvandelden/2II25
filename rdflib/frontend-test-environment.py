import rdflib, sha, re, os
from rdflib import ConjunctiveGraph as Graph
from rdflib import Namespace, Literal

store = rdflib.ConjunctiveGraph()  

foaf = Namespace("http://xmlns.com/foaf/0.1/")
edocol = Namespace("http://edocol.com/namespace/1.0/")
ns = dict(edocol=Namespace("http://edocol.com/namespace/1.0/"))

achternaam = "van Delden"
outformat = 'xml'
#outformat = 'python'

g = Graph()

g.add((Literal("1"), foaf['Person'], Literal("Etienne")))
g.add((Literal("2"), foaf['name'], Literal("Edin")))
g.add((Literal("3"), foaf['name'], Literal("Anson")))
g.add(("Etienne", foaf['lastName'], Literal(achternaam) ))

# example:
for row in g.query("""SELECT ?name
                      WHERE { ?id foaf:lastName ?name .}""", 
                   initNs=dict(foaf=Namespace("http://xmlns.com/foaf/0.1/"))):
            print "name: %s" % row

