from gettext import find
import requests
from bs4 import BeautifulSoup

def beautifulSoup(formName, url = None):
  try:
    if url:
      request = requests.get(url)
      soup = BeautifulSoup(request.content, 'html.parser')
      return soup
    else:
      url = createUrl(formName)
      request = requests.get(url)
      soup = BeautifulSoup(request.content, 'html.parser')
      return soup
  except requests.exceptions.RequestException:
    print('Error: Could not request from url | beautifulSoup()')

def createUrl():
  url = 'https://apps.irs.gov/app/picklist/list/priorFormPublication.html?resultsPerPage=200&sortColumn=sortOrder&indexOfFirstRow=0&criteria=&value=&isDescending=false'
  return url

def findTable(formName):
  url = createUrl(formName)
  soup = beautifulSoup('', url)
  table = soup.find('table', { 'class': 'picklist-dataTable' })
  list = table.find_all('tr', { 'class': ['odd', 'even'] })
  return list
