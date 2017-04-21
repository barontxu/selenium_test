'''
function to create browser
'''
from selenium import webdriver
from base import BrowserBase
import operators as op
from element import *

PROXY = [
]
# driver =
# webdriver.PhantomJS(desired_capabilities=dcap,service_args=service_args)

class Browser(BrowserBase):
    '''create a broser with log'''
    log = {}

    def __init__(self, task_name):
        self.driver = webdriver.PhantomJS()
        self.task_name = task_name

    @property
    def current_url(self):
        return self.driver.current_url

    def save_to_log(self, dic):
        '''save info to doc'''
        for each in dic.keys():
            try:
                self.log[each].append(dic[each])
            except:
                self.log[each] = [dic[each]]


class BrowserFirefox(Browser):
    '''create a broser with log'''
    log = {}

    def __init__(self, task_name):
        self.driver = webdriver.Firefox()
        self.task_name = task_name
