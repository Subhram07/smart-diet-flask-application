from replit import db
from main.py import name
from main.py import age
from main.py import bmi

print(name)
db['name'] = name
db['age'] = age
db['bmi'] = bmi

#this is for deleting keys
for key in db.keys():
      del db[key]
      if key not in db:
        print("Value deleted successfully.")