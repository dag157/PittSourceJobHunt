import requests
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

#browser = webdriver.Chrome(executable_path=r"")



def main():
    chromedriver = os.getcwd()+"/chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chromedriver)
    driver.get("https://cfopitt.taleo.net/careersection/pitt_student_int/jobsearch.ftl?lang=en&portal=18200023232#")

    username = driver.find_element_by_id("username")
    password = driver.find_element_by_id("password")

    username.clear()
    password.clear()

    #
    #
    # ENTER USERNAME AND PASSWORD HERE
    #
    #

    username.send_keys("")
    password.send_keys("")

    driver.find_element_by_name("_eventId_proceed").click()
    #driver.find_element_by_xpath("//select[@name='device']/option[text()='iOS']").click()
    #dropdown = driver.find_element_by_id("password")
    select = Select(driver.find_element_by_name("device"))
    #select.select_by_index(1)
    select.select_by_value('phone2')

    #pause(20000)

    response = requests.get("https://cfopitt.taleo.net/careersection/pitt_student_int/jobsearch.ftl?lang=en&portal=18200023232#")
    soup = BeautifulSoup(response.text, features="html.parser")
    print(soup)
    #driver.quit()


if __name__ == '__main__':
    main()
