from gettext import find
import requests
from bs4 import BeautifulSoup

### Finds the table within the URL and returns a list of all forms ###
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

# Iterate through all pages of forms
def pageTracker(formName):
  soup = beautifulSoup(formName)
  try:
    numPageViewed = soup.find('th', { 'class': 'NumPageViewed' })
    attachments = numPageViewed.find_all('a')
    pages = []
    if not attachments: return
    for attachment in attachments:
      if attachment.text.isNumeric():
        pages.append(attachment.text)
    return max(pages)
  except Exception:
    print('Error: No results | pageTracker()')

### View results in terminal as JSON ###
def createJson(formName):
  results = {}
  date = []
  allPages = int(pageTracker(formName))
  # Filter for exact name on all pages
  for page in range(allPages):
    list = findTable(formName, page * 200)
    for row in list:
      formNameMatch = row.find('a', string = '{}'.format(formName))
      if formNameMatch:
        results['productNumber'] = row.find('a').text
        results['title'] = row.find('td', { 'class': 'MiddleCellSpacer' }).text.strip()
        date.append(row.find('td', { 'class': 'EndCellSpacer' }).text.strip())
      if date:
        results['minYear'] = min(date)
        results['maxYear'] = max(date)
      else:
        print('Error: No results | jsonView()')
      return results

def jsonView(forms):
  results = []
  for form in forms:
    results.append(createJson(form))
  return results
