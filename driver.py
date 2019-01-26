import time
import requests
import os
import datetime
import heapq
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# browser = webdriver.Chrome(executable_path=r"")
keywords = ["Programmer", "Programming", "Software"]
limit = 5
job_ids = []
job_dict = {}
job_list = []


class job_object():

    def __init__(self, organization, title, link, age, pid, date_str):
        self.organization = organization
        self.title = title
        self.link = link
        self.age = age
        self.pid = pid
        self.date_str = date_str

    def __lt__(self, other):
        return self.age > other.age


def main():
    chromedriver = os.getcwd() + "/chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chromedriver)
    driver.get("https://cfopitt.taleo.net/careersection/pitt_student_int/jobsearch.ftl?lang=en&portal=18200023232#")

    username = driver.find_element_by_id("username")
    password = driver.find_element_by_id("password")

    username.clear()
    password.clear()
    # driver.implicitly_wait(20)
    time.sleep(20)
    #
    #
    # ENTER USERNAME AND PASSWORD HERE
    #
    #
    '''
    We can figure this out later, couldn't test main functionality so I just put in a 20 second time delay for now.

    username.send_keys("")
    password.send_keys("")

    driver.find_element_by_name("_eventId_proceed").click()
    #driver.find_element_by_xpath("//select[@name='device']/option[text()='iOS']").click()
    #dropdown = driver.find_element_by_id("password")
    select = Select(driver.find_element_by_name("device"))
    #select.select_by_index(1)
    select.select_by_value('phone2')

    #pause(20000)
    '''
    response = requests.get(
        "https://cfopitt.taleo.net/careersection/pitt_student_int/jobsearch.ftl?lang=en&portal=18200023232#")

    time.sleep(1)

    for keyword_search in keywords:
        page = 1
        keyword = driver.find_element_by_id("KEYWORD")
        keyword.clear()
        keyword.send_keys(keyword_search)
        time.sleep(1)
        driver.find_element_by_id("search").click()
        time.sleep(1)
        while (page <= limit):
            soup = BeautifulSoup(driver.page_source.encode("utf-8"), features="html.parser")

            ul = soup.find('table', {'id': 'jobs'})
            time.sleep(1)

            for li_tag in ul.find_all('tr'):
                id = li_tag.get("id")
                if id == None:
                    continue

                if id in job_ids:
                    continue

                anchor = li_tag.find("a")
                details = li_tag.find_all('div', attrs={'class': 'absolute'})

                date_title_count = 0
                job_organzation = ""
                job_title = ""
                date_str_temp = ""

                for div_row in details:
                    date_title_count += 1

                    if date_title_count == 1:
                        job_title = div_row.get('title')
                    if date_title_count == 2:
                        job_organzation = div_row.get('title')
                    if date_title_count == 3:
                        date_str_temp = div_row.get('title')
                        date_title = datetime.datetime.strptime(div_row.get('title').replace(',', ''), '%b %d %Y').timestamp()


                url = "https://cfopitt.taleo.net" + anchor['href']
                job_ids.append(id)

                job_list.append(job_object(job_organzation, job_title, url, date_title, id, date_str_temp))

            page += 1
            next_page = soup.find("a", {"title": "Go to page " + str(page)})
            if next_page is not None:
                driver.find_element_by_id("next").click()

    heapq.heapify(job_list)
    while len(job_list) > 0:
        position = heapq.heappop(job_list)
        print(position.organization)
        print(position.title)
        print(position.link)
        #print(position.age)
        print(position.pid)
        print(position.date_str)
        print()

    # print(soup)

    # driver.quit()


if __name__ == '__main__':
    main()
