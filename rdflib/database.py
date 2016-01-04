# functies die we nog nodig hebben:
# - Laatste X pages

##########################################################
## 
## Imports
##
##########################################################

  # Dependencies imports
import sha, re, os, globals

  # Class imports
import usermethods
import documentmethods
import searchmethods
import tagmethods
#import commentmethods



##########################################################
## 
## Class: Database
##
##########################################################

class database():
  """
  Generally {type}methods-functions return a succes-boolean, and nothing else; 
  'get'-functions and search-functions are exceptions to this.

  For the creators of {type}methods-modules:
  Complementary properties are:
  {user1} follows {user2 of tag} - {user2 of tag} followed_by {user1}
  {user} interest {document} - {document} interests {user}
  {user} owner {document} - {document} owned_by {user}
  {user} contributor {document} - {document} contributed_to_by {user}
  
  """

##########################################################
## Initialisation
##########################################################
  #def __init__(self):
  #moet hier nog iets staan?

##########################################################
## Termination
##########################################################  
  def exitdb(self):
    globals.writedb()
    

  ##########################################################
  ##
  ## Methods: Document
  ##
  ## (For methods to get the comments on a document, see Comment methods)
  ##########################################################
  """ Used shorthands:
  pid: person identifier
  did: document identifier
  """

  def new_document(self, pid, name, content):
    return documentmethods.new(pid, name, content)
    
  def edit_document(self, did, name, content):
    return documentmethods.edit(did, name, content)

  def get_document(self, did):
    return documentmethods.get(did)
	
  def get_documents_from_user(self, pid):
    return documentmethods.getalluser(pid)
    
  def get_last_x_dox_from_user(self, pid, number):
    if len(get_documents_from_user(pid)) < number:
      return get_documents_from_user(pid)
    else:
      return get_documents_from_user(pid)[:number]
  
  def get_last_x_dox_general(self, number):
    return documentmethods.getlastxgeneral(number)
  
  def get_document_property(self, did, property):
    return documentmethods.get_property_value(did, property)
  
  def delete_document(self, did):
    return documentmethods.delete(did)
  
	
  ##########################################################
  ##
  ## Methods: User
  ##
  ## (For methods to get the comments on a document, see Comment methods)
  ##########################################################	
  def new_user(self, name, password, email):
    return usermethods.new(name, password, email)
	
  def delete_user(self, id):
    return usermethods.delete(id)
  
  # for properties with only 1 value (for ex. name)
  def set_user_property_value(self, id, property, value):
    return usermethods.setpropertyvalue(id, property, value)
	
  # for properties with multiple values (for ex. diplomas, although these aren't in here now)
  def add_user_property_value(self, id, property, value):
    return usermethods.addpropertyvalue(id, property, value)

  def delete_user_property_value(self, id, property):
    return usermethods.deletepropertyvalue(id, property)
    
  def delete_specific_user_property_value(self, id, property, value):
    return usermethods.deletespecific(id, property, value)
	
  def get_all_user_info(self, id):
    return usermethods.getallinfo(id)

  def get_user_property_value(self, id, property):
    return usermethods.getpropertyvalue(id, property)
	
  def follow_user(self, follower_id, followed_id):
	  return usermethods.follow(follower_id, followed_id)
    
  def get_userid_from_email(self, email):
    return usermethods.fromemail(email)
    
  def get_userid_from_other_property(self, property, value):
    return usermethods.fromproperty(property, value)    
	
  ##########################################################
  ##
  ## Methods: Search
  ##
  ## (For methods to get the comments on a document, see Comment methods)
  ##########################################################

  def search_document(self, arg):
    # geef arg van de vorm [eigenschap, waarde]
	  # returnt een array [document]
    return searchmethods.documents(arg)
	
  # nog te doen?
  def search_user(self, arg):
    # geef arg van de vorm [eigenschap, waarde]
	  # returnt een array [user]
    return searchmethods.users(arg)
    

  ##########################################################
  ##
  ## Methods: Tags
  ##
  ## (Add a tag to a document by calling set_{type}_property)
  ##########################################################
  
  def create_tag(self, tag):
    return tagmethods.add(tag)
    
  def tag_document(self, tag, documentid):
    return tagmethods.tag(tag, documentid)
	
  def remove_tag_document(self, tag, documentid):
    return tagmethods.remove(tag, documentid)
	
  def delete_tag(self, tag):
    return tagmethods.delete(tag)
    
  def follow_tag(self, id, tag):
    return tagmethods.follow(id, tag)
    
  def get_tagged(self, tag):
    return tagmethods.get(tag)

	
  ##########################################################
  ##
  ## Methods: Comments
  ##
  ## 
  ##########################################################
  #def add_comment_user(self, comment, id, poster_id):
  #  return commentmethods.add(comment, id, poster_id)
	
  #def add_comment_document(self, comment, document, poster_id):
  #  return commentmethods.add(comment, document, poster_id)
	
  #def remove_comment(self, id):
  #  return commentmethods.remove(id)	

  #def get_comments_on_user(self, id):
	# returnt een array [comment]  
  #  return commentmethods.commentsonuser(id)

  #def get_comments_on_document(self, id):
	# returnt een array [comment] 
  #  return commentmethods.commentsondocument(id)

  #def get_comments_by_user(self, id):
	# returnt een array [comment] 
  # return commentsmethods.commentsbyuser(id)=======
	#return commentsmethods.commentsbyuser(id)
  
### Termination
#
#
  def exitdb(self):
    globals.writedb()
    
if __name__== '__main__':
  db = database()
  #print db.new_user('jippie', 'asdf', 'geb@aren.taal')
  print db.set_user_property_value('1', 'email', 'asdf@asdf.asdf')
  print 'getvalue email:'
  print db.get_user_property_value('1', 'email')
  print 'delete:'
  print db.delete_specific_user_property_value('1', 'email', 'asdf@asdf.asdf')
  print 'setvalue email what:'
  print db.set_user_property_value('1', 'asdf', 'what@asdf.asdf')
  print 'getvalue asdf:'
  print db.get_user_property_value('1', 'asdf')
  exit()

