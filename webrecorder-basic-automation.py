#webrecorder basic automation script
#install selenium and chromedriver
#input your information and preferences in variables that are commented out as settings

import os, csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

# settings ------------
timeosec = 10 #in seconds
username = '' #webrecorder username
password = ''#webrecorder password
loadingTime = 10 #seconds you want to wait to make sure that the amount of bytes of the website you want to record has been the same value (for making sure the webstite you want to record is loaded)
chromedriverPath = '//Library/Application Support/Google/chromedriver' #your path to chromedriver
#----------------------

browser = webdriver.Chrome(executable_path=chromedriverPath)
browser.get('https://webrecorder.io/')
try:
	WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="bs-navbar-collapse"]/ul/li[1]/a')))
except TimeoutException:
	print("timed out waiting for the webrecorder page to load")
	browser.quit()
browser.find_element_by_xpath('//*[@id="bs-navbar-collapse"]/ul/li[1]/a').click()
try:
	WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="username"]')))
except TimeoutException:
	print("timed out waiting for the login popup to load")
	browser.quit()
usernameinput = browser.find_element_by_xpath('//*[@id="username"]')
passwordinput = browser.find_element_by_xpath('//*[@id="password"]')
usernameinput.send_keys(username)
time.sleep(1)
passwordinput.send_keys(password)
login = browser.find_element_by_xpath('//*[@id="loginform"]/button')
login.click()
try:
	WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="bs-navbar-collapse"]/ul/li[3]/a')))
except TimeoutException:
	print("timed out waiting for the navigation bar page to load")
	browser.quit()
with open('urls.txt','rb') as file:
	reader = csv.reader(file)
	for index,url in enumerate(file):
		url.strip()
		if index==0:
			search = browser.find_element_by_xpath("/html/body/div[1]/div[3]/form/div[1]/input")
			search.send_keys(url)
			print "recording request submitted"
		else:
		 	search = browser.find_element_by_xpath("/html/body/header/div/div[1]/div[1]/form/div/input")
			search.send_keys(url)
		try:
			WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH,'/html/body/header/div/div[1]/div[1]/span/span')))
		except TimeoutException:
			print("timed out waiting for the record page load")
			print url
			continue
		loadedBytes = browser.find_element_by_xpath('/html/body/header/div/div[1]/div[1]/span/span').get_attribute('innerHTML')
		print loadedBytes
		time.sleep(loadingTime)
		finalLoadedBytes = browser.find_element_by_xpath('/html/body/header/div/div[1]/div[1]/span/span').get_attribute('innerHTML')
		while loadedBytes != finalLoadedBytes:
			loadedBytes = browser.find_element_by_xpath('/html/body/header/div/div[1]/div[1]/span/span').get_attribute('innerHTML')
			time.sleep(loadingTime)
		browser.find_element_by_xpath('/html/body/header/div/div[1]/div[1]/div/button[1]')
		browser.get('https://webrecorder.io/' + username + '/%E6%9C%AA%E6%9D%A5%E4%BD%95%E6%9D%A5%E4%B8%BB%E9%A2%98vr%E5%B1%95%E5%8E%85/$new')