### User methods:
# TODO: van een user opvragen: wie volg hem/haar?

import globals
import re    
    
edocol = globals.edocol
Literal = globals.Literal

#######################################################################            
# hulpfuncties           
def newuserid():

  results = globals.g.query("""
                SELECT ?id 
                WHERE {?id edocol:type edocol:person . }""", 
                initNs=globals.ns).serialize(format="python")
  print "results: %s" % results
  
  # return
  return  globals.getnewid(results)

  
#######################################################################
# voeg een nieuwe user toe  
def new(name, password, email):
  # add new user
  id = newuserid()
  
  email1 = ''
  email2 = ''
  email3 = ''
  phase = 1
  
  for char in email:
    if phase == 3:
      if char == '.':
        assert False, 'email address cannot contain more than 1 dot.'
      else:
        email3 = email3 + char  
    if phase == 2:
      if char == '.':
        phase = 3
      else:
        email2 = email2 + char  
    if phase == 1:
      if char == '@':
        phase = 2
      else:
        email1 = email1 + char

  assert (fromemail(email) == []), 'email address already in use'


  globals.g.add( (edocol[id], edocol["type"], edocol["person"])    )   # add the person
  globals.g.add( (edocol[id], edocol["name"], edocol[name])         ) # add the name
  globals.g.add( (edocol[id], edocol["email1"], edocol[email1])       )	# add the email address 
  globals.g.add( (edocol[id], edocol["email2"], edocol[email2])       )	# add the email address  
  globals.g.add( (edocol[id], edocol["email3"], edocol[email3])       )	# add the email address    
  globals.g.add( (edocol[id], edocol["password"], edocol[password]) ) # add the password

  #Write database
  globals.writedb()
  return id

#######################################################################
# verander de waarde van een 1-waarde-eigenschap van een user (bijexample zn naam)
def setpropertyvalue(id, property, value):
  assert (not (value in getpropertyvalue(id, property))), 'already has that value for that property'

  
  if property == 'email':
    email1 = ''
    email2 = ''
    email3 = ''
    phase = 1

    for char in value:
      if phase == 3:
        if char == '.':
          assert False, 'email address cannot contain more than 1 dot.'
        else:
          email3 = email3 + char  
      if phase == 2:
        if char == '.':
          phase = 3
        else:
          email2 = email2 + char  
      if phase == 1:
        if char == '@':
          phase = 2
        else:
          email1 = email1 + char 
          
    assert ((not (property == email1)) and (not (property == email2)) and (not (property == email3))), 'cannot set email# properties directly'
          
    globals.g.set( (edocol[id], edocol['email1'], edocol[email1]) )   
    globals.g.set( (edocol[id], edocol['email2'], edocol[email2]) )   
    globals.g.set( (edocol[id], edocol['email3'], edocol[email3]) )   
    
  else:
    globals.g.set( (edocol[id], edocol[property], edocol[value]) )    
  
  #Write database
  globals.writedb()
  return True 
  
#######################################################################
# add a value to a multi-value property of a user ( for ex. diplomas)
def addpropertyvalue(id, property, value):

  assert (not (value in getpropertyvalue(id, property))), 'already has that value for that property'

  assert not (property == 'email'), 'a user can have only one email address at a time. use "set_user_property_value" to change it'
  assert ((not (property == email1)) and (not (property == email2)) and (not (property == email3))), 'cannot set email# properties directly' 
 
  globals.g.add( (edocol[id], edocol[property], edocol[value]) )    
  
  #Write database
  globals.writedb()
  return True

#######################################################################
# ask for a (list of) value(s) of a property
def getpropertyvalue(id, property):

  assert ( globals.g.predicate_objects(id) <> [] ), 'User does not exist or does not have that property'

  if property == 'email':
    results = []
    emailnlist = ['email1', 'email2', 'email3']
    for p in emailnlist:
      results = results + globals.g.query("""
              SELECT ?id ?p ?value 
              WHERE {edocol:%s edocol:%s ?value . 
                     ?id ?p ?value .}""" % (id, p), 
              initNs=globals.ns).serialize('python')
      
    output = []  
    for row in results:
      if (row[0] == edocol[id]) and (row[1] == edocol['email1']):
        output = output + [row]
        break
    for row in results:
      if (row[0] == edocol[id]) and (row[1] == edocol['email2']):
        output = output + [row]
        break
    for row in results:
      if (row[0] == edocol[id]) and (row[1] == edocol['email3']):
        output = output + [row]
        break
    print output 
    output = globals.parse_pyformat_many(output)
    print output
    output = output[0][2] + '@' + output[1][2] + '.' + output[2][2] 

    #Write database
    globals.writedb()
    return output
    
  else:
    # find all info on property of user id
    results = globals.g.query("""
                  SELECT ?id ?p ?value 
                  WHERE {edocol:%s edocol:%s ?value . 
                         ?id ?p ?value .}""" % (id, property), 
                  initNs=globals.ns).serialize('python')                                                                                  
  
    output = []
    for row in results:
      if (row[0] == edocol[id]) and (row[1] == edocol[property]):
        output = output + [row]
  
    #Write database
    globals.writedb()
    return globals.parse_pyformat_many(globals.individual(output))

#######################################################################
# follow a user: doesn't have much use yet, but will.
def follow(follower_id, followed_id):

  assert (not (followed_id in getpropertyvalue(follower_id, 'follows'))), 'already following that user'
  assert (not follower_id == followed_id), 'what? you cannot follow yourself! that is crazy!'
  assert globals.g.predicate_objects(followed_id)<>[], 'the user which you are trying to follow does not exist'

  globals.g.add((edocol[follower_id], edocol["follows"], edocol[followed_id])) 
  
  #Write database
  globals.writedb()
  return True

#######################################################################
# delete a user and all outgoing relationships, but not the ingoing ones.
def delete(id):		            
  
  # find all properties of user id
  targets = globals.g.query( """
                SELECT ?id ?p ?v 
                WHERE { edocol:%s ?p ?v .
                        ?id ?p ?v .}""" % id, 
                initNs=globals.ns).serialize('python')   
  
  # deletes all references from user (including all data) while leaving references to the id intact.   
  for row in targets:
    if row[0] == edocol[id]:
      globals.g.remove(row)
    
  #Write database
  globals.writedb()
  return globals.parse_pyformat_many(globals.individual(targets))

#######################################################################
# remove all values of a property of a user
def deletepropertyvalue(id, property):
                                                              
  for row in globals.g.objects(edocol[id], edocol[property]):
    globals.g.remove( (edocol[id], edocol[property], row) )  
    
  #Write database
  globals.writedb()
  return True 
  
#######################################################################
# remove 1 value of a property of a user
def deletespecific(id, property, value):
      
  for entry in getpropertyvalue(id, property):
    if value in entry:
      assert True,'no such value to delete'  
      
  globals.g.remove( (edocol[id], edocol[property], edocol[value]) )  
    
  #Write database
  globals.writedb()
  return True 

#######################################################################
# get all information about a user (the output is a bit messy)
def getallinfo(id):   
  
  # find all properties of user id
  targets = globals.g.query( """
                SELECT ?id ?p ?v 
                WHERE { edocol:%s ?p ?v .
                        ?id ?p ?v .}""" % id, 
                initNs=globals.ns).serialize(format='python')                                                   
  results = []

  
  for row in targets:
    if row[0] == edocol[id]:
      results = results + [row]

  #Write database
  globals.writedb()
  return globals.parse_pyformat_many(globals.individual(results))
  
#######################################################################
# 
def fromproperty(property, value):  
 
  # find all properties of user id
  target = globals.g.query( """
                SELECT ?id
                WHERE { ?id edocol:%s edocol:%s .}""" % (property, value), 
                initNs=globals.ns).serialize(format='python')  
 
  globals.writedb() 
  return globals.parse_pyformat_one(target)  
  
#######################################################################
# 
def fromemail(email):  
 
  email1 = ''
  email2 = ''
  email3 = ''
  phase = 1
  
  for char in email:
    if phase == 3:
      if char == '.':
        assert False, 'email address cannot contain more than 1 dot.'
      else:
        email3 = email3 + char  
    if phase == 2:
      if char == '.':
        phase = 3
      else:
        email2 = email2 + char  
    if phase == 1:
      if char == '@':
        phase = 2
      else:
        email1 = email1 + char 
 
  # find all properties of user id
  target = globals.g.query( """
                SELECT ?id
                WHERE { ?id edocol:email1 edocol:%s .
                        ?id edocol:email2 edocol:%s .
                        ?id edocol:email3 edocol:%s .}""" % (email1, email2, email3), 
                initNs=globals.ns).serialize(format='python')  
 
  globals.writedb() 
  return globals.parse_pyformat_one(target)