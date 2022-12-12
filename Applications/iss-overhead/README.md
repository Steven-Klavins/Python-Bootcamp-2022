# ISS Overhead

A script that notifies you via email when the [ISS](https://en.wikipedia.org/wiki/International_Space_Station) passes overhead.

http://api.open-notify.org/

### Setup

**Set your latitude and longitude**
If you don't know your latitude and longitude you can visit https://www.latlong.net/ to find out.
```
MY_LAT = 51.507351  # Your latitude
MY_LONG = -0.127758  # Your longitude
```
**Set your email, SMTP provider and password**
Your SMTP provider and password will depend on the mail service your using.
```
EMAIL = "sample-email@email.com"
PASSWORD = os.environ.get("SMTP_PASSWORD")
SMTP_PROVIDER = "smtp.gmail.com"
```

####Install the packages
This script only requires 5 packages. You can install them either directly through a package manager such as [pip](https://pypi.org/project/pip/) or via your IDE if choice. This project was created in [Python 3.9.1](https://www.python.org/downloads/release/python-391/), however, it should run in the most recent releases.

### Running The Script
This script of course can be run locally, however, for a quick and easy way of deploying it you can use [PythonAnywhere](https://www.pythonanywhere.com/).
