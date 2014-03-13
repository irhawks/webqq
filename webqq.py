#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding: utf-8

import re
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class MainWindow:
	"""
	Web QQ main window object.
	"""
	def __init__(self, element):
		self.window = element
		self.mode = ''

	def select_tab(self, tabname):
		"""
		switch to group or buddy tab.
		"""
		if tabname == 'buddy':
			element = self.window.find_element_by_id('EQQ_TabBuddyList')
			element.click()
			self.mode = 'buddy'
		if tabname == 'group':
			element = self.window.find_element_by_id('EQQ_TabGroupList')
			element.click()
			self.mode = 'group'

	def __find_group(self, groupname):
		"""
		find group with group name of groupname
		"""
		self.select_tab('group')
		
		group_list = self.window.find_elements_by_class_name(
				'EQQ_GroupList_Group')
		group = None
		for g in group_list:
			elem = g.find_element_by_class_name('EQQ_GroupList_Name')
			if elem.text == groupname:
				group = g
				break
		return group

	def chat_group(self, groupname):
		"""
		Open chatbox for groupname
		"""
		mode = self.mode
		self.select_tab('group')
		group = self.__find_group(groupname)
		group.click()
		self.select_tab(mode)

	def __get_buddy_class_list(self):
		"""
		Open chatbox for buddyname
		"""
		self.select_tab('buddy')
		
		# cannot be the same as open_group because buddy can be collapsed.
		parent = self.window.find_element_by_id('EQQ_buddyList')
		collapsed = parent.find_elements_by_xpath(
				'//div[@class="EQQ_listClassHeadCollapsed"]')
		extended = parent.find_elements_by_xpath(
				'//div[@class="EQQ_listClassHeadExpand expand"]')
		buddy_class = collapsed + extended
		return buddy_class

	def __get_buddy_class_name(self, buddy_class):
		"""
		get buddy class name through buddy_class
		e.g. self.__get_buddy_class_name(self.__get_buddy_class_list()[0])
		"""
		self.select_tab('buddy')
		elem = buddy_class.find_element_by_class_name('EQQ_Class_className')
		return elem.text

	def __get_buddy_class(self, classname):
		"""
		get buddy class identifier through buddy class name
		"""
		self.select_tab('buddy')

		class_list = self.__get_buddy_class_list()
		buddy_class = None
		for c in class_list:
			testname = self.__get_buddy_class_name(c)
			testname = testname.strip()
			if testname == classname:
				buddy_class = c
				break

		return buddy_class

	def get_buddy_class_name_list(self):
		"""
		Get buddy class name list
		"""
		mode = self.mode
		self.select_tab('buddy')

		class_list = self.__get_buddy_class_list()
		result = [self.__get_buddy_class_name(c).strip() 
				for c in class_list]

		self.select_tab(mode)
		return result

	def __open_buddy_class(self, buddy_class):
		"""
		open buddy class tab from buddy_class
		"""
		self.select_tab('buddy')

		c = buddy_class.get_attribute('class')
		if c == 'EQQ_listClassHeadCollapsed':
			buddy_class.click()

	def open_buddy_class(self, classname):
		"""
		open buddy class of name "classname"
		e.g. self.open_buddy_class('unknown')
		"""
		class_id = self.__get_buddy_class(classname)
		self.__open_buddy_class(class_id)

	def __get_buddy_list(self, buddy_class):
		"""
		get buddy list from buddy_class
		e.g. self.__get_buddy_list(__get_buddy_class_list()[0])
		"""
		mode = self.mode
		self.select_tab('buddy')

		self.__open_buddy_class(buddy_class)

		head_id = buddy_class.get_attribute('id')
		body_id = re.sub('Head', 'Body', head_id)
		buddy_class_body = self.window.find_element_by_id(body_id)
		buddy_list = buddy_class_body.find_elements_by_class_name(
				'EQQ_BuddyList_Buddy')
		self.select_tab(mode)
		#print "buddy list is", buddy_list
		return buddy_list

	def __get_buddy_name(self, buddy):
		"""
		get buddy name from a buddy xml element
		e.g. __get_buddy_name(__get_buddy_list(C)[0])
		"""
		name = buddy.find_element_by_class_name('EQQ_BuddyList_Nick')
		#print "buddy_name is ", name.text
		return name.text

	def __get_buddy(self, buddyname):
		"""
		get buddy from a buddyname.
		return buddy_class and buddy.
		"""
		self.select_tab('buddy')
		buddy_class_list = self.__get_buddy_class_list()
		for buddy_class in buddy_class_list:
			self.__open_buddy_class(buddy_class)
			buddy_list = self.__get_buddy_list(buddy_class)
			for buddy in buddy_list:
				if self.__get_buddy_name(buddy) == buddyname:
					return buddy_class, buddy

		return None
	
	def get_buddy_name_list(self, classname=None):
		"""
		get buddy name list from classname
		e.g. self.get_buddy_name_list('unknown')
		"""
		if classname != None:
			buddy_class = self.__get_buddy_class(classname)
			self.__open_buddy_class(buddy_class)
			buddy_list = self.__get_buddy_list(buddy_class)
			return [self.__get_buddy_name(b) for b in buddy_list]
		else: # get all buddies
			name_list = []
			class_list = self.__get_buddy_class_list()
			for buddy_class in class_list:
				self.__open_buddy_class(buddy_class)
				buddy_list = self.__get_buddy_list(buddy_class)
				name_list+=[self.__get_buddy_name(b) for b in buddy_list]
			return name_list

	def chat_buddy(self, buddyname):
		"""
		open and chat to somebody.
		"""
		buddy_class, buddy = self.__get_buddy(buddyname)
		self.__open_buddy_class(buddy_class)
		buddy.click()

	def click():

		self.window.click()

class ChatWindow:
	"""
	Opeartions on Chat window.
	"""
	def __init__(self, window):
		self.window = window

		element = self.window.find_element_by_class_name('chatBox_mainName')
		self.name = element.text

		element = self.window.find_element_by_class_name('chatBox_nameArea')
		string = element.get_attribute('id')
		self.id = re.search('(\d+)', string).group(0)

	def input(self, message):
		element = self.window.find_element_by_class_name('rich_editor_div')
		element.send_keys(message)

	def clear_input(self):
		element = self.window.find_element_by_class_name('rich_editor_div')
		element.clear()

	def send(self, message=''):
		self.input(message)
		button_id = 'chatBox_sendMsgButton_%s' % self.id
		element = self.window.find_element_by_id(button_id)
		element.click()

	def clear(self):

		button_id = 'chatBox_clearButton_%s' % self.id
		element = self.window.find_element_by_id(button_id)
		element.click()

	def receive(self):

		received_id = 'chatBox_msgList_%s' % self.id
		element = self.window.find_element_by_id(received_id)
		return element.text

	def close(self):

		button_id = 'chatBox_closeButton_%s' % self.id
		element = self.window.find_element_by_id(button_id)
		element.click()

	def click(self):

		self.window.click()


class WebQQDriver:

	def __init__(self):
		"""
		load a session in selenium firefox with firebug support
		"""
		fp = webdriver.FirefoxProfile('./profile')
		self.__browser = webdriver.Firefox(firefox_profile=fp)

	def do_login(self, username, password):

		self.__browser.get('http://web.qq.com')
		
		element = self.__browser.find_element_by_xpath(
			'//a[@class="img_wrap" and @href="./webqq.html"]')
		
		element.click()
		time.sleep(5)
		element = self.__browser.find_element_by_xpath('//img[@alt="QQ"]')
		element.click()
		self.__browser.switch_to_frame('ifram_login')
		
		element = self.__browser.find_element_by_id('u')
		element.clear()
		element.send_keys(username)
		element = self.__browser.find_element_by_id('p')
		element.send_keys(password)
		element = self.__browser.find_element_by_id('login_button')
		element.click()
		self.__browser.switch_to_default_content()
		
		self.main_window = self.__get_main_window()
		self.chat_list = self.__update_chat_window()


	def __get_main_window(self):

		mw = self.__browser.find_elements_by_class_name('window')[0]
		return MainWindow(mw)

	def __update_chat_window(self):

		ws = self.__browser.find_elements_by_class_name('window')
		result = []
		for w in ws:
			if w.find_elements_by_class_name('chatBox_mainName') != []:
				result.append(ChatWindow(w))
		return result

	def update(self):
		"""
		update chat window list
		"""
		self.chat_list = self.__update_chat_window()

	def close(self):
		"""
		close browser, lose connection.
		"""
		self.__browser.close()

if __name__ == '__main__' :

	driver = WebQQDriver()
	time.sleep(3)
	driver.do_login('2927670573', 'yourpassword')
	time.sleep(5)
	mw = driver.main_window
	mw.open_buddy_class(u'应用数学')
