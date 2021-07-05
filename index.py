import json
import os.path

from os import path
from Business.ShopBusiness import ShopBusiness
from Model.Shop import Shop

READING_USERS_PATH = 'Utils/users.json'

# startTime = (datetime.now()).replace(hour = 15, minute = 59, second = 50) # El tesoro
# startTime = (datetime.now()).replace(hour = 19, minute = 59, second = 50) # Saldos USA

def GetUsersFromFile():
  with open(READING_USERS_PATH) as jsonFile:
    shop = json.load(jsonFile)
    shopObject = Shop(**shop)
    jsonFile.close()

  return shopObject
    
if __name__ == '__main__':  
  ShopBusiness(GetUsersFromFile())

