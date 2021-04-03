from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

URL = 'http://elib.tcd.ie/login?url=https://advance.lexis.com/nexis?&identityprofileid=69Q2VF60797'
# 'http://elib.tcd.ie/login?url=https://advance-lexis-com.elib.tcd.ie/search/?pdmfid=1519360&crid=73e961c4-b6cf-4228-87f3-3a5117b9fd21&pdsearchterms=GameStop+Corp&pdstartin=hlct%3A1%3A1&pdcaseshlctselectedbyuser=false&pdtypeofsearch=searchboxclick&pdsearchtype=SearchBox&pdoriginatingpage=bisnexishome&pdqttype=or&pdpsf=&pdquerytemplateid=&ecomp=kx7hkkk&earg=pdpsf&prid=cc72eba0-7bea-4baa-a492-8b83c7747f19'

opts = Options()
# opts.set_headless()
# assert opts.headless # Operating in headless mode
# browser = Firefox(options=opts)
browser = Firefox()
browser.get(URL)

login_form = browser.find_element_by_id('loginform')
name = login_form.find_element_by_name('user')
name.send_keys('mcguinmi')
name = login_form.find_element_by_name('pass')
name.send_keys()
login_form.submit()

# TODO