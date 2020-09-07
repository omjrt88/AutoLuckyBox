# import atexit
import os
import sys
import wget
import requests
import time
import pause
from multiprocessing import Pool
from datetime import datetime  
from selenium.webdriver.common.by import By
from clint.textui import progress
from Library.Site import SiteMetaData
from selenium.webdriver.support import expected_conditions as EC

baseUrl = "https://www.fichascr.com/GeneradorFichas.php?CodTienda=4"
Users = [
  {
    "user": "omjrt88@gmail.com", 
    "password": "!234s678"
  },
  {
    "user": "omjrt88@hotmail.com", 
    "password": "!234s678"
  },
  {
    "user": "chinasr15@hotmail.com", 
    "password": "123456"
  }
]

def InitiateProgram():
  try:
    #Worker(Users[0])
    with Pool(len(Users)) as p:
      p.map(Worker, Users)
      p.terminate()
      p.join()

  except Exception as e:
    print("ERROR, Starting again...")
    print(e)

def Worker(user):
  site = SiteMetaData(baseUrl, True, False)
  WaitUntil5()
  Doloop(site, user)
  
def WaitUntil5():
  startTime = (datetime.now()).replace(hour = 16, minute = 59, second = 50)
  print("Wait until: ")
  print(startTime)
  pause.until(startTime)

def Doloop(site, user):
  print("Starting loop!")
  DoLogin(site, user["user"], user["password"])
  CheckResults(site, user)

def CheckResults(site, user):
  if site.findElement(By.ID, 'bGenerar'):
    print("Buttom found it!")
    Generar(site, user)
  elif "email con el código QR" in site.getDriver().Instance.page_source:
    Completed(site, user)
  elif "Reenviar Email" in site.getDriver().Instance.page_source:
    Completed(site, user)
  elif "503" in site.getDriver().Instance.page_source:
    GoAgain(site, user)
  else:
    GoAgain(site, user)

def Generar(site, user):
  print("Logged, Starting to generate..."+ user["user"])
  site.clickBy(By.ID, 'bGenerar')
  CheckResults(site, user)

def Completed(site, user):
  print("Did it, check Email "+ user["user"])
  currentDate = (datetime.now()).strftime("%d_%B_%Y")
  #time.sleep(5)
  site.getDriver().Instance.get_screenshot_as_file(user["user"]+"_"+currentDate+".png")
  Close(site)

def Close(site):
  site.closeThisPage()
  #sys.exit(0)

def GoAgain(site, user):
  print("Trying again...")
  site.getDriver().Instance.get(baseUrl)
  Doloop(site, user)

def DoLogin(site, user, password):
  site.setTextBy(By.ID, 'txtEmail', user)
  site.setTextBy(By.ID, 'txtClave', password)
  site.clickBy(By.XPATH, '//input[@value="Ingresar"]')
    
if __name__ == '__main__':  
  InitiateProgram()
