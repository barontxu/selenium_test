'''
include operations of safari
'''
# -*- coding: utf-8 -*-
import hashlib
import os
import time
from datetime import datetime
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from base import BrowserBase
from element import *
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

PROXY = [
]

class TimeoutError(Exception):
        pass

class BaseOp(BrowserBase):
    '''include base function'''
    def __init__(self):
        pass


class OpenUrl(BaseOp):
    '''openUrl'''
    def __init__(self, browser, url):
        browser.driver.get(url)
        browser.save_to_log({'ops': ('OpenUrlOp', url)})

open_url = OpenUrl


class Wait(BaseOp):
    '''wait for several seconds in browser '''
    def __init__(self, browser, times):
        wait_for(times)
        # browser.driver.implicitly_wait(times)

wait = Wait


class WaitUntilLoaded(BaseOp):
    '''until loaded'''
    def __init__(self, browser, time_out, op, *arg):
        driver = browser.driver
        last_html = driver.page_source
        op(browser, *arg)
        tick = datetime.now()
        while True:
            if driver.page_source != last_html and \
               driver.execute_script('return document.readyState;')=='complete':
                break
            else:
                time.sleep(0.2)
            if datetime.now() - tick > time_out:
                raise TimeoutError('Timeout Boom!')
        print "end"

wait_until_loaded = WaitUntilLoaded


class WaitForSthShow(BaseOp):
    '''until loaded'''
    def __init__(self, browser, time_out, elem_exp):
        tick = datetime.now()
        while not there_is(browser, elem_exp):
            print there_is(browser, elem_exp)
            time.sleep(0.2)
            if (datetime.now() - tick).total_seconds() > time_out:
                raise TimeoutError('Timeout Boom!')

wait_for_sth_show = WaitForSthShow


class FillForm(BaseOp):
    '''to fill form'''
    def __init__(self, browser, expression, types):
        xpath = set_xpath(input_parse(expression))
        elem = browser.driver.find_element_by_xpath(xpath)
        elem.send_keys(types)

fill_form = FillForm


class Click(BaseOp):
    '''click the element founded'''
    def __init__(self, browser, expression):
    # browser.driver.findElement(By.cssSelector(".dataLabel,.dataLabelWide");
        xpath = set_xpath(input_parse(expression))
        elem = browser.driver.find_element_by_xpath(xpath)
        elem.click()

click = Click


class Hover(BaseOp):
    '''perform hover in the element founded'''
    def __init__(self, browser, expression):
    # browser.driver.findElement(By.cssSelector(".dataLabel,.dataLabelWide");
        xpath = set_xpath(input_parse(expression))
        elem = browser.driver.find_element_by_xpath(xpath)
        hover = ActionChains(browser.driver).move_to_element(elem)
        hover.perform()

hover = Hover


class ScrollBy(BaseOp):
    '''scroll page'''
    def __init__(self, browser, scroll_pos=10000):
        browser.driver.execute_script("window.scrollBy(0, Y);".replace('Y',
                                                                       str(scroll_pos)))

scroll_by = ScrollBy


class Back(BaseOp):
    '''back to previous'''
    def __init__(self, browser):
        browser.driver.back()

back = Back


class Forward(BaseOp):
    '''forward to next'''
    def __init__(self, browser):
        browser.driver.forward()

forward = Forward


class SendKeys(BaseOp):

    def __init__(self, elem, string):
        elem.send_keys(string)

send_keys = SendKeys


def wait_for(condition_function, time_out=10):
    '''wait time'''
    start_time = time.time()
    while time.time() < start_time + time_out:
        if condition_function():
            return True
        else:
            time.sleep(0.1)
    raise Exception(
        'Timeout waiting for {}'.format(condition_function.__name__)
    )


class WaitForPageLoad(object):
    'wait for loading'

    def __init__(self, browser, time_out=10):
        self.browser = browser
        self.time_out = time_out

    def __enter__(self):
        self.old_page = self.browser.find_element_by_tag_name('html')

    def page_has_loaded(self):
        '''judge if page has loaded'''
        new_page = self.browser.find_element_by_tag_name('html')
        return new_page.id != self.old_page.id

    def __exit__(self, *_):
        wait_for(self.page_has_loaded)
