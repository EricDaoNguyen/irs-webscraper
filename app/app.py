import functions as scrape
import os

def main():
  # Clears terminal
  clear = lambda: os.system('clear')
  user_input = input('\n\n\nTo view forms in JSON, type "json".\nTo download forms into PDF files, type "download".\n> > > ')
  if user_input == 'json':
    clear()
    print('Please enter form names, separated by commas and a space (ex. Form W-2, Publ 1, etc).')
    forms_input = input('\n> > > ')
    forms = forms_input.split(', ')
    clear()
    scrape.view_json(forms)
    print('\n\n\n')
    main()
  if user_input == 'download':
    clear()
    print('Please enter form name (ex. Form W-2).')
    form_input = input('\n> > > ')
    clear()
    print('Please enter the year(s) you would like to download in YYYY-YYYY format (ex. 2018-2020).')
    range_input = input('> > > ')
    years = scrape.date_range(range_input)
    scrape.pdf_download(form_input, years)
    print('Download complete!\n\n\n')
    main()

if __name__ == '__main__':
  main()
