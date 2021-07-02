import os
import sys
import wget
import requests
import time
import pause
import signal
import json
import os.path

from os import path
from multiprocessing import Pool
from functools import partial
from datetime import datetime  
from selenium.webdriver.common.by import By
from clint.textui import progress
from Library.Site import SiteMetaData
from Model.Shop import Shop, User
from selenium.webdriver.support import expected_conditions as EC

READING_USERS_PATH = 'Utils/users.json'

# startTime = (datetime.now()).replace(hour = 15, minute = 59, second = 50) # El tesoro
# startTime = (datetime.now()).replace(hour = 19, minute = 59, second = 50) # Saldos USA

def InitiateProgram():
  try:
    shopUsers = GetUsersFromFile()
    WaitUntil5(shopUsers.hour-1, 59, 30)
    with Pool(processes=len(shopUsers.users)) as p:
      WorkerWithUrl=partial(Worker, baseUrl=shopUsers.baseUrl, hour=shopUsers.hour)
      p.map(WorkerWithUrl, shopUsers.users)
      p.terminate()
      p.join()

  except Exception as e:
    print("ERROR, Starting again...")
    print(e)

def signal_handler(signal, frame):
  print('You pressed Ctrl+C!')
  sys.exit(0)
  print('Terminated!!')

def Worker(user, baseUrl, hour):
  signal.signal(signal.SIGTERM, signal_handler)
  signal.signal(signal.SIGINT, signal_handler)
  print(baseUrl)
  site = SiteMetaData(baseUrl, True, False)
  CheckSecurePage(site)
  WaitUntil5(hour-1, 59, 55)
  Doloop(site, user, baseUrl)
  
def WaitUntil5(hour, minute, second):
  startTime = (datetime.now()).replace(hour = hour, minute = minute, second = second)
  print("Wait until: ")
  print(startTime)
  pause.until(startTime)

def Doloop(site, user, baseUrl):
  print("Starting loop!")
  DoLogin(site, user.user, user.password)
  CheckResults(site, user, baseUrl)

def CheckResults(site, user, baseUrl):
  if site.findElement(By.ID, 'bGenerar'):
    print("Buttom found it!")
    Generar(site, user)
  elif "503" in site.getDriver().Instance.page_source:
    GoAgain(site, user, baseUrl)
  elif "Page not" in site.getDriver().Instance.page_source:
    GoAgain(site, user, baseUrl)
  elif "email con el código QR" in site.getDriver().Instance.page_source:
    Completed(site, user)
  elif "Reenviar Email" in site.getDriver().Instance.page_source:
    Completed(site, user)
  else:
    GoAgain(site, user, baseUrl)

def Generar(site, user):
  print("Logged, Starting to generate..."+ user["user"])
  site.clickBy(By.ID, 'bGenerar')
  CheckResults(site, user)

def Completed(site, user):
  print("Did it, check Email "+ user["user"])
  currentDate = (datetime.now()).strftime("%d_%B_%Y")
  site.getDriver().Instance.get_screenshot_as_file(user["user"]+"_"+currentDate+".png")
  Close(site)

def Close(site):
  site.closeThisPage()

def GoAgain(site, user, baseUrl):
  print("Trying again...")
  site.getDriver().Instance.get(baseUrl)
  Doloop(site, user, baseUrl)

def DoLogin(site, user, password):
  site.setTextBy(By.ID, 'txtEmail', user)
  site.setTextBy(By.ID, 'txtClave', password)
  site.clickBy(By.XPATH, '//input[@value="Ingresar"]')

def CheckSecurePage(site):
  if "ERR_CERT_COMMON_NAME_INVALID" in site.getDriver().Instance.page_source:
    if site.findElement(By.ID, 'details-button'):
      site.clickBy(By.ID, 'details-button')
      site.clickBy(By.ID, 'proceed-link')

def GetUsersFromFile():
  with open(READING_USERS_PATH) as jsonFile:
    shop = json.load(jsonFile)
    shopObject = Shop(**shop)
    jsonFile.close()

  return shopObject
    
if __name__ == '__main__':  
  InitiateProgram()
