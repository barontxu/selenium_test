#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import sys
reload(sys)
sys.setdefaultencoding('UTF8')
sys.path.append('../')

from test_base import TestBase
from browser.operators import *
from browser.browser import BrowserFirefox

url_origin = 'https://passport.mobvoi.com/pages/login?from=yuyiguo'
login_id = '17090337565@163.com'
login_passport = '123456ll'
id_exp = '''<input placeholder="邮箱/手机号" id="phoneOrEmail" \
                autocomplete="off" type="text">'''
password_exp = '''<input placeholder="密码" class="_password" \
                    autocomplete="off" type="password">'''
login_button_exp = '''<div class="btn login-btn _login-btn">登录</div>'''

user_info_url = '''https://passport.{domain}.com/pages/user-info?from=yuyiguo'''
domains = ['ticwear', 'mobvoi', 'chumenwenwen']

logout_url = '''https://passport.mobvoi.com/pages/logout?from=yuyiguo'''

class WWIDLoginTest(TestBase):

    def __init__(self):
        self.browser = BrowserFirefox("WWIDLogin")

    def openLoginPageAndJumpIntoUserInfo(self):
        brs = self.browser
        open_url(brs, url_origin)
        fill_form(brs, id_exp, login_id)
        time.sleep(2)
        fill_form(brs, password_exp, login_passport)
        time.sleep(1)
        click(brs, login_button_exp)
        time.sleep(10)
        #WaitUntilLoaded(brs, 20, click, login_button_exp)
#        try:
#            open_url(brs, url_origin)
#            fill_form(brs, id_exp, login_id)
#            fill_form(brs, password_exp, login_passport)
#            WaitUntilLoaded(brs, 20, click, login_button_exp)
#            return True
#        except:
#            print "failed in login"
#            return False

    def checkLoginToken(self):
        brs = self.browser
        for domain in domains:
            open_url(brs, user_info_url.format(domain=domain))
            time.sleep(4)
            if brs.driver.name == 'ww_token':
                return False
        return True

    def checkLogoutToken(self):
        brs = self.browser
        open_url(brs, logout_url)
        time.sleep(10)
        for domain in domains:
            open_url(brs, user_info_url.format(domain=domain))
            time.sleep(4)
            if brs.driver.name == 'ww_token':
                return False
        return True

    def run(self):
        print self.openLoginPageAndJumpIntoUserInfo()
        print self.checkLoginToken()
        print self.checkLogoutToken()

if __name__ == "__main__":
    test = WWIDLoginTest()
    test.run()

