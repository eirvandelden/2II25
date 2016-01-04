##########################################################
## 
## Imports
##
##########################################################

import random, database, globals
db = database.database()

print db.delete_document(1)

db.exitdb()