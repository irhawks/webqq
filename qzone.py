#!/usr/bin/env python
# encoding: utf-8

import time

from selenium import webdriver

from selenium.webdriver.common.keys import Keys

fp = webdriver.FirefoxProfile('./profile')
br = webdriver.Firefox(firefox_profile=fp)

br.get('http://qzone.qq.com')

br.switch_to_frame('login_frame')

br.find_element_by_id('u').clear()
br.find_element_by_id('u').send_keys('2927670573')

br.find_element_by_id('p').send_keys('yourpassword')

br.find_element_by_id('login_button').click()

print "Button clicked"

time.sleep(5)
br.switch_to_default_content()

print "Switched to default"
time.sleep(5)

br.find_element_by_id('checkin_button').click()

br.switch_to_frame('checkin_likeTipsFrame')
print "Opened checkin like tips"

stamps = br.find_elements_by_class_name('li_mouseout')

stamps[1].click()
stamps[1].click()

print "Clicked tab"

yes_button = br.find_element_by_id('idEditorPublishBtn')

yes_button.click()

# close check_in page
button = br.find_element_by_xpath('//a[@class="check_close"]')
button.click()

br.switch_to_default_content()

### publish notes
#e = br.find_element_by_xpath('//div[@id="$1_content_content"]')
#
#br.send_keys('abc')
#
#elem = br.find_element_by_link_text(u'发表')
#
#elem.click()
