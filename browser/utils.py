'''
include utils
'''
# -*- coding: utf-8 -*-
import hashlib
from bs4 import BeautifulSoup as bs
from lxml import etree
import os
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')
parser = etree.HTMLParser()


def safe_mkdir(path):
    try:
        os.mkdir(path)
    except:
        pass
