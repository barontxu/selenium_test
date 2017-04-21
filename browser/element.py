'''
include element_handle function of safari like find a element or its siblings
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

# def input_check(expression):


def input_parse(expression):
    '''
    for a img tag like
    input_parse(''<img id="J_Itemlist_Pic_40227190967" class="J_ItemPic img">'')
    input_parse(''<span class="J_ItemPic img">11</span>'')
    or if you not sure what the tag is , use
    input_parse(''<UNKNOWN_TAG id="J_Itemlist_Pic_40227190967" class="J_ItemPic img">'')
    or a dict that contains the info above
    '''
    if isinstance(expression, dict):
        return expression
    try:
        soup = bs(expression)
        tag = soup.children.next().next()[0]
        dic = tag.attrs
        if not tag.text == u'':
            dic['text'] = tag.text
        if not tag.name == 'UNKNOWN_TAG':
            dic['tag_name'] = tag.name
        return dic
    except:
        print 'parse failed'
        return 'failed'


def find_parent_elem(browser_elem):
    '''get the parent in html of the elem '''
    try:
        return browser_elem.find_element_by_xpath('..')
    except:
        return 'failed'

def find_all_child_elems(browser_elem):
    '''get siblings of the elem, return a list'''
    return browser_elem.find_elements_by_css_selector("*")

def find_all_child_elems_recursively(browser_elem):
    '''get siblings of the elem, return a list'''
    return_children = []
    direct_children = browser_elem.find_elements_by_css_selector("*")
    return_children = return_children + direct_children
    for child in direct_children:
        return_children = return_children + find_all_child_elems_recursively(child)

def find_child_elems(browser_elem, expression):
    input_dict = input_parse(expression)
    xpath = set_xpath(input_dict)
    try:
        elems = browser_elem.find_elements_by_xpath(xpath)
        match_text = []
        if 'text' in input_dict.keys():
            for each in elems:
                if each.text == input_dict['text']:
                    match_text.append(each)
            return match_text
        else:
            return elems
    except:
        return False

def find_siblings(browser_elem):
    '''get siblings of the elem'''
    return get_child_elems(get_parent_elem(browser_elem))


def get_attrs(browser, browser_elem):
    attrs = browser.driver.execute_script('''var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index)
                                     { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; 
                                     return items;''', browser_elem)
    return attrs

def set_xpath(input_dict):
    if 'tag_name' in input_dict.keys():
        xpath = "//" + input_dict['tag_name']
    else:
        xpath = "//" + "*"
    for each in input_dict.keys():
        if each == 'text' or each == 'tag_name':
            continue
        if isinstance(input_dict[each], list):
            value = u' '.join(input_dict[each])
        else:
            value = input_dict[each]
        if value == '':
            xpath += '[@{}]'.format(each)
        else:
            xpath += '[@{}=\'{}\']'.format(each, value)
        print xpath
    return xpath


def find_the_elements(browser, expression):
    input_dict = input_parse(expression)
    xpath = set_xpath(input_dict)
    try:
        elems = browser.driver.find_elements_by_xpath(xpath)
        match_text = []
        if 'text' in input_dict.keys():
            for each in elems:
                if each.text == input_dict['text']:
                    match_text.append(each)
            return match_text
        else:
            return elems
    except:
        return False


def there_is(browser, expression):
    input_dict = input_parse(expression)
    xpath = set_xpath(input_dict)
    try:
        elems = browser.driver.find_elements_by_xpath(xpath)
        if 'text' in input_dict.keys():
            for each in elems:
                if each.text == input_dict['text']:
                    return True
            return False
        else:
            if elems != []:
                return True
            else:
                return False
    except:
        print "exception"
        return False


def save_with_extract(browser, expression, wanted_lis):
    '''
    for a tag like:
    <img id="J" class="J_ItemPic img" src="//g-searc" data-src="//g-search"
    alt="dsad">
    save_with_extract(my_safari, "<img class=\"J_ItemPic img\">",
                                 [data-src, alt] )
    return with a dict with two list
    '''
    elems = find_the_elements(expression)
    dic = {}
    for each in wanted_lis:
        dic[each] = []
        for elem in elems:
            try:
                dic.append(elem.attrs[each])
            except:
                continue


def safe_mkdir(path):
    '''safely make dir'''
    if not os.path.exists(os.path.abspath(path)):
        os.mkdir(os.path.abspath(path))


def save_html(browser, output_path='./output/'):
    '''save html in hashed file_name'''
    safe_mkdir(output_path)
    source = browser.driver.page_source.encode('utf-8')
    file_name = browser.task_name + \
        hashlib.md5(source).hexdigest()
    file_path = os.path.join(os.path.abspath(output_path), file_name)
    print file_path
    with open(file_path, 'w') as f:
        f.write(browser.driver.page_source)


# def there_is_not(browser, expression):


# def get_elem_has(browser, expression):
