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

def test_countries_zones(driver):
    driver.get(" http://localhost/litecart/admin/?app=countries&doc=countries")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()
    is_element_present(driver, By.XPATH, '//h1[contains(.,"Countries")]')
    countries_zones_column_list = driver.find_elements_by_xpath('//tr[@class="row"]')
    #starts from checking countries are sorted
    countries_name_list = []
    for country in countries_zones_column_list:
        countries_column_list = country.find_elements_by_xpath('.//td[5]')
        for country_name in countries_column_list:
            countries_name_list.append(country_name.text)
    sorted_countries_name_list = countries_name_list
    sorted_countries_name_list.sort()
    if sorted(countries_name_list) == sorted_countries_name_list:
        print('\nCountries list is sorted')
    else:
        print("\nCountries list isn't sorted")
    #find countries with zones
    country_with_zones = []
    for row in countries_zones_column_list:
        zone = row.find_element_by_xpath('.//td[6]')
        if int(zone.text) > 0:
            country = row.find_element_by_xpath('.//td[5]')
            country_with_zones.append(country.text)
    print('Countries with more than 0 zones: ' + str(country_with_zones))
    #open selected countries pages and check zones are sorted
    for country in country_with_zones:
        driver.find_element_by_link_text(country).click()
        is_element_present(driver, By.XPATH, '//h1[contains(.,"Edit Country")]')
        zones_list = driver.find_elements_by_xpath('//table[@id="table-zones"]//tr/td[3]')
        zones_name_list = []
        for i in zones_list[1:]:
            zones_name_list.append(i.text)
        sorted_zones_name_list = zones_name_list
        sorted_zones_name_list.sort()
        if sorted(zones_name_list) == sorted_zones_name_list:
            print("\nZones for country " + str(country) + " are sorted")
        else:
            print("\nZones for country " + str(country) + " aren't sorted")
        driver.find_element_by_xpath('//button[contains(@name,"cancel")]').click()
        is_element_present(driver, By.XPATH, '//h1[contains(.,"Countries")]')
    #test geo zones
    driver.get("http://localhost/litecart/admin/?app=geo_zones&doc=geo_zones")
    geo_zones_column_list = driver.find_elements_by_xpath('//tr[@class="row"]/td[3]')
    geo_zones = []
    for name in geo_zones_column_list:
        geo_zones.append(name.text)
    for country in geo_zones:
        driver.find_element_by_link_text(country).click()
        is_element_present(driver, By.XPATH, '//h1[contains(.,"Edit Geo Zone")]')
        zones_list = driver.find_elements_by_xpath('//table[@id="table-zones"]//tr/td[3]//option[@selected="selected"]')
        zones_name_list = []
        for i in zones_list[1:]:
            zones_name_list.append(i.text)
        sorted_zones_name_list = zones_name_list
        sorted_zones_name_list.sort()
        if sorted(zones_name_list) == sorted_zones_name_list:
            print("\nGeo Zones for country " + str(country) + " are sorted")
        else:
            print("\nGeo Zones for country " + str(country) + " aren't sorted")
        driver.find_element_by_xpath('//button[contains(@name,"cancel")]').click()
        is_element_present(driver, By.XPATH, '//h1[contains(.,"Geo Zones")]')
