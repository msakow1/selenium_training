import pytest
import string
import random

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    #print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd

def is_element_present(driver, *args):
  try:
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((args)))
    return True
  except NoSuchElementException:
    return False

def random_string(maxlen):
    symbols = string.ascii_letters
    return "".join(random.choice(symbols) for i in range (maxlen))

def random_number(maxlen):
    number = string.digits
    return "".join(random.choice(number) for i in range (maxlen))

def test_add_new_product(driver):
    driver.get("http://localhost/litecart/admin/?app=catalog&doc=catalog")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()
    is_element_present(driver, By.XPATH, '//h1[contains(.,"Catalog")]')
    driver.find_element_by_xpath('//a[contains(.,"Add New Product")]').click()
    is_element_present(driver, By.XPATH, '//h1[contains(.,"Add New Product")]')
    #GENERAL tab
    driver.find_element_by_css_selector('a[href="#tab-general"]').click()
    is_element_present(driver, By.XPATH, '//a[@href="#tab-general"]/ancestor::li[@class="active"]')
    driver.find_element_by_name("status").click()
    name = random_string(10)
    code = "".join([random_string(2), random_number(2)])
    quantity = random_number(3)
    driver.find_element_by_name("name[en]").send_keys(str(name))
    driver.find_element_by_name("code").send_keys(str(code))
    driver.find_element_by_name("product_groups[]").click()
    driver.find_element_by_name("quantity").clear()
    driver.find_element_by_name("quantity").send_keys(str(quantity))
    date_valid_from = driver.find_element_by_name("date_valid_from")
    date_valid_from.click()
    date_valid_from.send_keys("2018")
    date_valid_from.send_keys(Keys.ARROW_LEFT)
    date_valid_from.send_keys("01")
    date_valid_from.send_keys(Keys.ARROW_LEFT)
    date_valid_from.send_keys(Keys.ARROW_LEFT)
    date_valid_from.send_keys("01")
    date_valid_to = driver.find_element_by_name("date_valid_to")
    date_valid_to.click()
    date_valid_to.send_keys("2019")
    date_valid_to.send_keys(Keys.ARROW_LEFT)
    date_valid_to.send_keys("01")
    date_valid_to.send_keys(Keys.ARROW_LEFT)
    date_valid_to.send_keys(Keys.ARROW_LEFT)
    date_valid_to.send_keys("01")
    #INFORMATION tab
    driver.find_element_by_css_selector('a[href="#tab-information"]').click()
    is_element_present(driver, By.XPATH, '//a[@href="#tab-information"]/ancestor::li[@class="active"]')
    manufacturer = Select(driver.find_element_by_name("manufacturer_id"))
    manufacturer.select_by_value("1")
    keywords = random_string(10)
    short_desc = random_string(10)
    desc = "".join([random_string(5)," ",random_string(10)," ",random_string(15)])
    head = random_string(5)
    meta = random_string(5)
    driver.find_element_by_name("keywords").send_keys(str(keywords))
    driver.find_element_by_name("short_description[en]").send_keys(str(short_desc))
    driver.find_element_by_css_selector("div.trumbowyg-editor").click()
    driver.find_element_by_css_selector("div.trumbowyg-editor").send_keys(str(desc))
    driver.find_element_by_name("head_title[en]").send_keys(str(head))
    driver.find_element_by_name("meta_description[en]").send_keys(str(meta))
    #PRICES tab
    driver.find_element_by_css_selector('a[href="#tab-prices"]').click()
    is_element_present(driver, By.XPATH, '//a[@href="#tab-prices"]/ancestor::li[@class="active"]')
    purchase_price = random_number(3)
    driver.find_element_by_name("purchase_price").click()
    driver.find_element_by_name("purchase_price").send_keys(str(purchase_price))
    currency = Select(driver.find_element_by_name("purchase_price_currency_code"))
    currency.select_by_value("USD")
    driver.find_element_by_name("gross_prices[USD]").click()
    driver.find_element_by_name("gross_prices[USD]").send_keys(str(purchase_price))
    driver.find_element_by_name("gross_prices[EUR]").click()
    driver.find_element_by_name("gross_prices[EUR]").send_keys(str(purchase_price))
    driver.find_element_by_name("save").click()
    #Check product was added
    is_element_present(driver, By.XPATH, '//h1[contains(.,"Catalog")]')
    is_element_present(driver, By.XPATH, '//td[contains(.,' + name + ')]')

