import pytest
import string
import random

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    #print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd

def is_element_present(driver, *args):
  try:
    wait = WebDriverWait(driver, 5)
    wait.until(EC.presence_of_element_located((args)))
    return True
  except NoSuchElementException:
    return False

def is_url_present(driver):
  try:
    wait = WebDriverWait(driver, 5)
    wait.until(EC.url_to_be("http://localhost/litecart/en/"))
    return True
  except:
    pass
    return False


def new_email_address(home_page_loaded):
    email = "".join([random_string(5), "@email.com"])
    driver.find_element_by_name("email").send_keys(str(email))
    driver.find_element_by_name("password").send_keys(str(password))
    driver.find_element_by_name("confirmed_password").send_keys(str(password))
    driver.find_element_by_name("create_account").click()
    return email

def random_string(maxlen):
    symbols = string.ascii_letters
    return "".join(random.choice(symbols) for i in range (maxlen))

def random_number(maxlen):
    number = string.digits
    return "".join(random.choice(number) for i in range (maxlen))

def test_create_new_customer(driver):
    driver.get("http://localhost/litecart/en/")
    is_element_present(driver, By.XPATH, '//div[@id="box-most-popular"]/h3[contains(.,"Most Popular")]')
    driver.find_element_by_link_text("New customers click here").click()
    is_element_present(driver, By.XPATH, '//div[@id="create-account"]/h1[contains(.,"Create Account")]')
    first_name = random_string(6)
    last_name = random_string(10)
    address1 = "".join(["Street ", random_string(10)," ",random_number(3)])
    postcode = "".join([random_number(2),"-",random_number(3)])
    city = random_string(8)
    phone = "".join(["+48", random_number(9)])
    email = "".join([random_string(5), "@email.com"])
    #email = "tucut1@email.com"
    password = str("1234")
    driver.find_element_by_name("firstname").send_keys(str(first_name))
    driver.find_element_by_name("lastname").send_keys(str(last_name))
    driver.find_element_by_name("address1").send_keys(str(address1))
    driver.find_element_by_name("postcode").send_keys(str(postcode))
    driver.find_element_by_name("city").send_keys(str(city))
    driver.find_element_by_name("phone").send_keys(str(phone))
    driver.find_element_by_name("email").send_keys(str(email))
    driver.find_element_by_name("password").send_keys(str(password))
    driver.find_element_by_name("confirmed_password").send_keys(str(password))
    driver.find_element_by_name("create_account").click()
    home_page_loaded = is_url_present(driver)
    while (home_page_loaded==False):
        #new_email_address(home_page_loaded)
        email = "".join([random_string(5), "@email.com"])
        driver.find_element_by_name("email").clear()
        driver.find_element_by_name("email").send_keys(str(email))
        driver.find_element_by_name("password").send_keys(str(password))
        driver.find_element_by_name("confirmed_password").send_keys(str(password))
        driver.find_element_by_name("create_account").click()
        home_page_loaded = is_url_present(driver)

    driver.find_element_by_link_text("Logout").click()
    driver.find_element_by_name("email").send_keys(str(email))
    driver.find_element_by_name("password").send_keys(str(password))
    driver.find_element_by_name("login").click()
    driver.find_element_by_link_text("Logout").click()
