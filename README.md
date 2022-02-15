# IRS Webscraper

#### Python version: 3.9.10

## Description
This application is a webscraper for the IRS website (https://apps.irs.gov/app/picklist/list/priorFormPublication.html) where the user is able to search for the form(s) and dates (in years) and can do one of two things, download the specific form into PDF files or view the form(s) as JSON within the terminal and should look like the following example:

```
[
  {
    "form_number": "Form W-2",
    "form_title": "Wage and Tax Statement (Info Copy Only)",
    "min_year": 1954,
    "max_year": 2021,
  }
]
```

## Instructions
If you haven't already, please install the [extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python).

In the terminal, type the following:
```
source env/bin/activate
pip install -r requirements.txt
```

Once the above steps are done, you can run the application in a few different ways:
* Right click the python file and select "Run Python File in Terminal" located at app/app.py.
* Open the app/app.py file in the text editor and open the Command Palette (Command+Shift+P on macOS and Ctrl+Shift+P on Windows/Linux).
  * Type and execute "Python: Run Python File in Terminal".
* Open the app/app.py file in the text editor and on the run button (play symbol on the top right of VSCode), click the arrow to the right of the play symbol and select "Run Python File".

Once the app starts, you will be redirected to the instructions within the terminal.

## Feedback
&nbsp;&nbsp;&nbsp;&nbsp;Overall this assignment was surprisingly difficult, however I enjoyed this assignment and the challenges it gave me! Although this was my first time getting my hands on Python, I learned a lot about the language, the different libraries, and how to use language to specifically scrape data from websites. Thank you for giving me this amazing opportunity to try your assignment and allow me to broaden my knowledge of the language!
