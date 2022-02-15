import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path

### BeautifulSoup and requests ###
def create_soup(form, url = None):
  try:
    if url:
      request = requests.get(url)
      soup = BeautifulSoup(request.content, 'html.parser')
      return soup
    else:
      url = create_url(form)
      request = requests.get(url)
      soup = BeautifulSoup(request.content, 'html.parser')
      return soup
  except requests.exceptions.RequestException as error:
    print('@create_soup() | ERROR: ' + error)

def create_url(form, index = 0):
  space_replaced_form = form.replace(' ', '+')
  url = 'https://apps.irs.gov/app/picklist/list/priorFormPublication.html?indexOfFirstRow={0}&sortColumn=sortOrder&value={1}+&criteria=formNumber&resultsPerPage=25&isDescending=false'.format(index, space_replaced_form)
  return url

# Iterates all the pages instead of a select number of pages
def view_all_pages(form):
  soup = create_soup(form)
  try:
    num_page_viewed = soup.find('th', { 'class': 'NumPageViewed' })
    attachments = num_page_viewed.find_all('a')
    if not attachments:
      return 1
    pages = []
    for each_attachment in attachments:
      if each_attachment.text.isnumeric():
        pages.append(each_attachment.text)
      return max(pages)
  except Exception as error:
    print('@viewAllPages() | ERROR: ' + error)

def search_table(form, page):
  url = create_url(form, page)
  soup = create_soup('', url)
  table = soup.find('table', { 'class': 'picklist-dataTable' })
  list = table.find_all('tr', { 'class': [ 'odd', 'even' ]})
  return list

### View as JSON in the terminal ###
# Filters out forms that do not match the user's input
def search_form(form):
  results = {}
  date = []
  all_pages = int(view_all_pages(form))
  for each_page in range(all_pages):
    table = search_table(form, each_page * 25)
    for each_row in table:
      string_match = each_row.find('a', string='{}'.format(form))
      if string_match:
        results['form_number'] = each_row.find('a').text
        results['form_title'] = each_row.find('td', { 'class': 'MiddleCellSpacer' }).text.strip()
        date.append(each_row.find('td', { 'class': 'EndCellSpacer' }).text.strip())
  if date:
    results['min_year'] = min(date)
    results['max_year'] = max(date)
  else:
    print('No results found.')
  return results

def view_json(forms):
    results = []
    for each_form in forms:
      results.append(search_form(each_form))
    print(json.dumps(results, indent = 2))
    return results

### Download PDFs ###
def create_pdf(file_name, request):
  file_name.parent.mkdir(parents = True, exist_ok = True)
  with file_name.open('wb') as file:
    for each_chunk in request.iter_content(chunk_size=1024):
      if each_chunk:
        file.write(each_chunk)

# Filters out dates that match user's input
def date_range(years):
  if len(years) != 9: print('Please enter in this format: YYYY-YYYY')
  results = []
  min_to_max = years.split('-')
  years = range(int(min_to_max[0]), int(min_to_max[1]) + 1)
  for each_year in years:
    results.append(each_year)
  return results

def pdf_download(form, dates):
  pages = int(view_all_pages(form))
  for each_page in range(pages):
    table = search_table(form, each_page * 25)
    for each_row in table:
      string_match = each_row.find('a', string='{}'.format(form))
      if string_match:
        years_match = each_row.find('td', { 'class': 'EndCellSpacer' }).text.strip()
        if int(years_match) in dates:
          link = each_row.find('a')['href']
          request = requests.get(link, stream = True)
          file = Path('{name}/{name} - {year}.pdf'.format(name = form, year = years_match))
          create_pdf(file, request)
