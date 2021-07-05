import os
import sys
import wget
import requests
import time
import pause
import signal

from multiprocessing import Pool
from functools import partial
from datetime import datetime  
from selenium.webdriver.common.by import By
from clint.textui import progress
from Library.Site import SiteMetaData
from Model.Shop import Shop, User
from selenium.webdriver.support import expected_conditions as EC

class ShopBusiness:
  
  def __init__(self, shopData):
    try:
      self.shopData = shopData
      # self.WaitUntil5(self.shopData.hour-1, 59, 30)
      with Pool(processes=len(self.shopData.users)) as p:
        WorkerWithUrl=partial(self.Worker, hour=self.shopData.hour)
        p.map(WorkerWithUrl, self.shopData.users)
        p.terminate()
        p.join()
    except Exception as e:
      print("ERROR, Starting again...")
      print(e)

  def signal_handler(self, signal, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)
    print('Terminated!!')

  def Worker(self, user, hour):
    signal.signal(signal.SIGTERM, self.signal_handler)
    signal.signal(signal.SIGINT, self.signal_handler)
    print(self.shopData.baseUrl)
    site = SiteMetaData(self.shopData.baseUrl, True, False)
    self.CheckSecurePage(site)
    # self.WaitUntil5(hour-1, 59, 55)
    self.Doloop(site, user)
    
  def WaitUntil5(self, hour, minute, second):
    startTime = (datetime.now()).replace(hour = hour, minute = minute, second = second)
    print("Wait until: ")
    print(startTime)
    pause.until(startTime)

  def Doloop(self, site, user):
    try:
      print("Starting loop!")
      self.DoLogin(site, user.user, user.password)
      self.CheckResults(site, user)
    except Exception as e:
      print(e)


  def CheckResults(self, site, user):
    if site.findElement(By.ID, 'bGenerar'):
      print("Buttom found it!")
      self.Generar(site, user)
    elif "503" in site.getDriver().Instance.page_source:
      self.GoAgain(site, user)
    elif "Page not" in site.getDriver().Instance.page_source:
      self.GoAgain(site, user)
    elif "email con el código QR" in site.getDriver().Instance.page_source:
      self.Completed(site, user)
    elif "Reenviar Email" in site.getDriver().Instance.page_source:
      self.Completed(site, user)
    else:
      self.GoAgain(site, user)

  def Generar(self, site, user):
    print("Logged, Starting to generate..."+ user["user"])
    site.clickBy(By.ID, 'bGenerar')
    self.CheckResults(site, user)

  def Completed(site, user):
    print("Did it, check Email "+ user["user"])
    currentDate = (datetime.now()).strftime("%d_%B_%Y")
    site.getDriver().Instance.get_screenshot_as_file(user["user"]+"_"+currentDate+".png")
    self.Close(site)

  def Close(self, site):
    site.closeThisPage()

  def GoAgain(self, site, user):
    print("Trying again...")
    site.getDriver().Instance.get(self.shopData.baseUrl)
    self.Doloop(site, user)

  def DoLogin(self, site, user, password):
    site.setTextBy(By.ID, 'txtEmail', user)
    site.setTextBy(By.ID, 'txtClave', password)
    site.clickBy(By.XPATH, '//input[@value="Ingresar"]')

  def CheckSecurePage(self, site):
    if "ERR_CERT_COMMON_NAME_INVALID" in site.getDriver().Instance.page_source:
      if site.findElement(By.ID, 'details-button'):
        site.clickBy(By.ID, 'details-button')
        site.clickBy(By.ID, 'proceed-link')