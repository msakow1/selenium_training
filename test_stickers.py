import pytest

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
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((args)))
    return True
  except NoSuchElementException:
    return False

def number_of_elements(driver, *args):
    return len(driver.find_elements(*args))

def sticker_per_product(driver):
    image = driver.find_elements_by_xpath("//img[contains(@alt,'Duck')]/..")
    length = len(image)
    for x in range(length):
        len(image[x].find_elements_by_xpath("//div[contains(@class,'sticker')]")) < 2


def test_stickers(driver):
    driver.get("http://localhost/litecart/en/")
    is_element_present(driver, By.XPATH, '//div[@id="box-most-popular"]/h3[contains(.,"Most Popular")]')
    sticker_per_product(driver)
    stickers_number = number_of_elements(By.CSS_SELECTOR, "div.sticker")
    print('Number of stickers on the page is %d' % stickers_number)
