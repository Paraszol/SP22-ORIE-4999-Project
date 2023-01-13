import csv, time

from bs4 import BeautifulSoup
from selenium import webdriver

wd = webdriver.Chrome('../chromedriver.exe')

def scrapeCourses(page, courses):
  f = open('LiberalStudies.csv', 'a', newline="")
  #https://stackoverflow.com/questions/3348460/csv-file-written-with-python-has-blank-lines-between-each-row
  #https://stackoverflow.com/questions/13203868/how-to-write-to-csv-and-not-overwrite-past-text
  writer = csv.writer(f)

  wd.get("https://apps.engineering.cornell.edu/liberalstudies/" + page + ".cfm")
  SCROLL_PAUSE_TIME = 5
  last_height = wd.execute_script('return document.body.scrollHeight')
  wd.execute_script('window.scrollTo(0, document.body.scrollHeight);')
  time.sleep(SCROLL_PAUSE_TIME)
  new_height = wd.execute_script('return document.body.scrollHeight')
  last_height = new_height

  src = wd.page_source
  soup = BeautifulSoup(src, 'lxml')

  # https://stackoverflow.com/questions/23377533/python-beautifulsoup-parsing-table

  data = []
  table = soup.find('table')
  table_body = table.find('tbody')

  rows = table_body.find_all('tr')
  for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele])  # Get rid of empty values
  data = data[1:]  # first element was empty

  courses[page] = []

  for course in data:
    writer.writerow([page, course[0], course[1], course[2]])
    courses[page].append([course[0], course[1], course[2]])

  f.close()

liberalStudies = ["CA", "HA", "KCM", "LA", "SBA", "CE", "ALC", "SCD", "HST", "ETM", "SSC", "GLC"]
liberalStudiesCourses = {}
for category in liberalStudies:
  scrapeCourses(category, liberalStudiesCourses)
# print(liberalStudiesCourses)