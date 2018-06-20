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


def test_product_page(driver):
    driver.get("http://localhost/litecart/en/")
    is_element_present(driver, By.XPATH, '//div[@id="box-most-popular"]/h3[contains(.,"Most Popular")]')
    #product name and prices
    main_page_product_details = driver.find_element_by_css_selector("div#box-campaigns li:first-child a")
    main_page_product_name = main_page_product_details.find_element_by_css_selector("div.name").text
    main_page_regular_price = main_page_product_details.find_element_by_css_selector("s.regular-price").text
    main_page_campaign_price = main_page_product_details.find_element_by_css_selector("strong.campaign-price").text
    #css styles for main page
    main_page_regular_price_text_color = main_page_product_details.find_element_by_css_selector("s.regular-price").value_of_css_property("color")
    main_page_regular_price_text_style = main_page_product_details.find_element_by_css_selector("s.regular-price").value_of_css_property("text-decoration-line")
    main_page_campaign_price_text_color = main_page_product_details.find_element_by_css_selector("strong.campaign-price").value_of_css_property("color")
    main_page_campaign_price_text_style = main_page_product_details.find_element_by_css_selector("strong.campaign-price").value_of_css_property("text-decoration-line")
    main_page_product_details.click()
    #check product details page
    is_element_present(driver, By.XPATH, '//h1[contains(.,"%s")]' % main_page_product_name)
    is_element_present(driver, By.XPATH, '//s[@class = "regular-price" and (contains(.,"%s"))]' % main_page_regular_price)
    is_element_present(driver, By.XPATH, '//strong[@class = "campaign-price" and (contains(.,"%s"))]' % main_page_campaign_price)
    product_regular_price_text_color = driver.find_element_by_css_selector("s.regular-price").value_of_css_property("color")
    product_regular_price_text_style = driver.find_element_by_css_selector("s.regular-price").value_of_css_property("text-decoration-line")
    product_campaign_price_text_color = driver.find_element_by_css_selector("strong.campaign-price").value_of_css_property("color")
    product_campaign_price_text_style = driver.find_element_by_css_selector("strong.campaign-price").value_of_css_property("text-decoration-line")

    if (main_page_regular_price_text_color == product_regular_price_text_color):
        print('\nThe color of the regular price text is the same on the main page and on the product details page')
    else:
        print('\nThe color of the regular price text is different on the main page and on the product details page')
    if (main_page_regular_price_text_style == product_regular_price_text_style):
        print('\nThe text style of the regular price is the same on the main page and on the product details page')
    else:
        print('\nThe text style of the regular price is different on the main page and on the product details page')
    if (main_page_campaign_price_text_color == product_campaign_price_text_color):
        print('\nThe color of the campaign price text is the same on the main page and on the product details page')
    else:
        print('\nThe color of the campaign price text is different on the main page and on the product details page')
    if (main_page_campaign_price_text_style == product_campaign_price_text_style):
        print('\nThe text style of the campaign price is the same on the main page and on the product details page')
    else:
        print('\nThe text style of the campaign price is different on the main page and on the product details page')
    #get_attribute(name)




