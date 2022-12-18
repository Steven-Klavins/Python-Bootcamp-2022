# Birthday Wisher

Never forget a birthday again! Using this script, you can automate birthday wishes for your friends and family via your SMTP provider. 

### Setup

**Update the birthdays.csv with your birthday list**
The rows in the birthdays.csv file has 5 collums name,email,year,month,and day.
For example, say you have an entry for someone called James, with an email of james@email.com and a birthdate of 29th November 1961. In the CSV file, enter the data in the following fashion. 

```
James,james@email.com,1961,11,29
```

**Set your email, SMTP provider and password**
Your SMTP provider and password will depend on the mail service your using.
```
EMAIL = "sample-email@email.com"
PASSWORD = os.environ.get("SMTP_PASSWORD")
SMTP_PROVIDER = "smtp.gmail.com"
```

**Add your own custom messages**
This script creates birthday messages by randomly selecting a template from the templates folder. Templates are stored in text format and the recipient's name is inserted on the first line at the [NAME] tag. 

For example:
```
Dear [NAME],

Happy birthday!

All the best for the year!

Steven
```
If you would like to add more than 3 custom templates make sure to number them appropriately, and follow the same naming convention as the examples ("letter_1.txt" ,"letter_2.txt", "letter_3.txt"). 

Additionally, update line 27 of main.py to select a random int in a range that corresponds to your number of letter templates. For example, if you had 4 letter templates it would be:

```
27 | template_path = f"letter_templates/letter_{random.randint(1, 4)}.txt"
```
####Install the packages
This script only requires 5 packages. You can install them either directly through a package manager such as [pip](https://pypi.org/project/pip/) or via your IDE if choice. This project was created in [Python 3.9.1](https://www.python.org/downloads/release/python-391/), however, it should run in the most recent releases.

### Running The Script
This script of course can be run locally, however, for a quick and easy way of deploying it you can use [PythonAnywhere](https://www.pythonanywhere.com/).