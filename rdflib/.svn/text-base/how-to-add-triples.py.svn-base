from rdflib import ConjunctiveGraph as Graph
from rdflib import Namespace, Literal

foaf = Namespace("http://xmlns.com/foaf/0.1/")

achternaam = "van Delden"

g = Graph()
g.add((Literal("1"), foaf['Person'], Literal("Etienne")))
g.add((Literal("2"), foaf['name'], Literal("Edin")))
g.add((Literal("3"), foaf['name'], Literal("Anson")))
g.add(("Etienne", foaf['lastName'], Literal(achternaam) ))

for row in g.query("""SELECT ?name
                      WHERE { ?id foaf:lastName ?name .}""", 
                   initNs=dict(foaf=Namespace("http://xmlns.com/foaf/0.1/"))):
            print "name: %s" % row