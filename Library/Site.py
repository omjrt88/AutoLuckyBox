# import atexit
import urllib.request
import sys
import time
import wget
import os, fnmatch
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, TimeoutException 
from selenium.webdriver.support import expected_conditions as EC

from . import Driver

class SiteMetaData:

	def __init__(self, url, setWait = False, headless = False):
		self.url = url
		self.initializeDriver(setWait, headless)
		# atexit.register(self.closePage, self)

	# Driver events
	def getDriver(self):
		return Driver

	def initializeDriver(self, setWait, headless = False):
		Driver.Initialize(headless)
		Driver.Instance.get(self.url)

	# @atexit.register
	def closePage():
		Driver.CloseDriver()

	def closeThisPage(self):
		Driver.CloseDriver()

	def AlertPresent(self):
		return EC.alert_is_present()

	def GetAlertText(self):
		alert = Driver.Instance.switch_to.alert
		text = alert.text
		alert.accept()
		return text

	def getReturnHistory(self, numberPages = 1):
		Driver.Instance.execute_script("window.history.go(-"+ numberPages +")")
		Driver.Instance.switch_to_default_content()

	# HTML Selenium Events or Functions
	def awaitAndReturn(self, searchType, searchValue, instanceObj = None):
		try:
			if instanceObj is None:
				instanceObj = Driver.Instance
			wait = WebDriverWait(instanceObj, 5)
			return wait.until(EC.presence_of_element_located((searchType, searchValue)))
		except Exception as e:
			return self.___itemsExceptions(e, searchValue)

	def availableElement(self, searchType, searchValue, instanceObj = None):
		if instanceObj is None:
			instanceObj = Driver.Instance
		return self.findElement(searchType, searchValue, instanceObj, True) != None

	def findElement(self, searchType, searchValue, instanceObj = None, avoidPrintMsgs=False):
		try:
			# print(searchValue)
			if instanceObj is None:
				instanceObj = Driver.Instance
				return self.awaitAndReturn(searchType, searchValue)

			return instanceObj.find_element(searchType, searchValue)
		except Exception as e:
			if avoidPrintMsgs:
				return None
			return self.___itemsExceptions(e, searchValue)

	def findElements(self, searchType, searchValue, instanceObj = None):
		if instanceObj is None:
			instanceObj = Driver.Instance
		try:
			return instanceObj.find_elements(searchType, searchValue)
		except Exception as e:
			return self.___itemsExceptions(e, searchValue)

	def changeToFrameFromRoot(self, frameName):
		Driver.Instance.switch_to_default_content()
		# Driver.Instance.switch_to.default_content()
		self.changeToFrame(frameName)
		
	def changeToFrame(self, frameName):
		Driver.Instance.switch_to.frame(Driver.Instance.find_element_by_name(frameName))

	def clickBy(self, searchType, itemKey, simulateClick = False):
		item = self.findElement(searchType, itemKey)
		if item != None:
			if (not bool(item.get_attribute('disabled'))):
				if (simulateClick):
					item.send_keys("\n")
				else:
					item.click()

	def clickCheckBoxBy(self, searchType, itemKey, value, instanceObj = None):
		if instanceObj is None:
			instanceObj = Driver.Instance
		item = self.findElement(searchType, itemKey, instanceObj)
		if item != None:
			if (not bool(item.get_attribute('disabled'))):
				try:
					if (item.is_selected() != value):
						item.click()
				except ElementNotVisibleException:
					instanceObj.execute_script('arguments[0].click();', item)

	def clickAllSimilars(self, searchType, itemKey, instanceObj = None):
		if instanceObj is None:
			instanceObj = Driver.Instance
		items = self.findElements(searchType, itemKey, instanceObj)

		for item in items:
			if item != None:
				if (not bool(item.get_attribute('disabled'))):
					item.click()

	def clickRadioButtonBy(self, searchType, itemKey):
		item = self.findElement(searchType, itemKey)
		if item != None:
			if (not bool(item.get_attribute('disabled'))):
				item.click()

	def selectDropdownOptionBy(self, searchType, itemKey, option, instanceObj = None):
		if instanceObj is None:
			instanceObj = Driver.Instance
		item = self.findElement(searchType, itemKey, instanceObj)
		if item != None:
			if (not bool(item.get_attribute('disabled')) and option != ''):
				select = Select(item)
				select.select_by_visible_text(option)

	def setJsTextBy(self, searchType, itemKey, text, instanceObj = None):
		if instanceObj is None:
			instanceObj = Driver.Instance
		try:
			item = self.findElement(searchType, itemKey, instanceObj)
			if item != None:
				if (not bool(item.get_attribute('disabled'))):
					item.click()
					item.send_keys(Keys.CONTROL, "a")
					item.send_keys(text)
		except Exception as e:
			return self.___itemsExceptions(e, itemKey)

	def setTextBy(self, searchType, itemKey, text, instanceObj = None):
		if instanceObj is None:
			instanceObj = Driver.Instance
		try:
			item = self.findElement(searchType, itemKey, instanceObj)
			if item != None:
				if (not bool(item.get_attribute('disabled'))):
					item.clear()
					item.send_keys(text)
		except Exception as e:
			return self.___itemsExceptions(e, itemKey)

	def getValueSelectDropdown(self, searchType, itemKey, instanceObj = None):
		try:
			if instanceObj is None:
				instanceObj = Driver.Instance
			item = self.findElement(searchType, itemKey, instanceObj)
			if item != None:
				if (not bool(item.get_attribute('disabled'))):
					select = Select(item)
					return select.first_selected_option.text
			return None
		except Exception as e:
			return self.___itemsExceptions(e, itemKey)

	def getTextBy(self, searchType, itemKey, instanceObj = None):
		if instanceObj is None:
			instanceObj = Driver.Instance
		try:
			item = self.findElement(searchType, itemKey, instanceObj)
			if item != None:
				return item.text
		except Exception as e:
			return self.___itemsExceptions(e, itemKey)

	def getValueBy(self, searchType, itemKey, instanceObj = None):
		if instanceObj is None:
			instanceObj = Driver.Instance
		try:
			item = self.findElement(searchType, itemKey, instanceObj)
			if item != None:
				return item.get_attribute('value')
		except Exception as e:
			return self.___itemsExceptions(e, itemKey)

	def getCheckBoxBy(self, searchType, itemKey, instanceObj = None):
		if instanceObj is None:
			instanceObj = Driver.Instance
		try:
			item = self.findElement(searchType, itemKey, instanceObj)
			if item != None:
				if (not bool(item.get_attribute('disabled'))):
					return item.is_selected()
		except Exception as e:
			return self.___itemsExceptions(e, itemKey)

	def _generateXpathRadioButtonSibling(self, radioGroupName,selectedOption):
		xpath = "//input[@type='radio'][@name='%s']" %(radioGroupName)
		txtFind = selectedOption.split(' ')
		txtFind = list(map(lambda x: "[contains(following-sibling::text(), '%s')]" %(x), txtFind))
		txtFind = ''.join(txtFind)
		return xpath + txtFind

	def ___itemsExceptions(self, exceptionType, exceptionItemkey):
		error = ''
		if isinstance(exceptionType, NoSuchElementException):
			error = "Element not found: %s" %(exceptionItemkey)
		elif isinstance(exceptionType, TimeoutException):
			error = 'Element not found: %s' %(exceptionItemkey)
		elif isinstance(exceptionType, ElementNotVisibleException):
			error = "Warning\\Error: %s" %(exceptionItemkey)
		else:
			error = "Error: %s, %s" %(str(exceptionType), exceptionItemkey)
		print(error)
		print(str(exceptionType))
		return None