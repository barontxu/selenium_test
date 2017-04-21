from selenium import webdriver
from selenium.webdriver.common.keys import Keys


service_args = [
    '--proxy=tel.lc.ignw.net:25',
    '--proxy-auth=megvii:face++',
    '--proxy-type=http',
    ]

#"http://username:password@proxy.host.com"
driver = webdriver.PhantomJS(service_args=service_args)
#driver = webdriver.PhantomJS()
driver.get("http://www.flickr.org")
from IPython import embed;embed()
# assert "Python" in driver.title
print driver.title
# elem = driver.find_element_by_name("q")
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
print driver.title
driver.implicitly_wait(10)
print driver.page_source
driver.close()
