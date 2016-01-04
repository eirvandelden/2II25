import database

db = database.database()

user_id = db.new_user('qwer', 'qewer', 'qwer@qwer.qwer')
print user_id
all_info = db. get_all_user_info(user_id)
print all_info