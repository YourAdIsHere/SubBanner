# SubBanner
Dynamically update YouTube banners with subscriber count.
## Notes
* You NEED both python2.7 and python3 to run this - submit a pull request if you want to update the second script to python3 or combine the 2
* Dependencies must be installed for the correct version of python.
## Dependencies
### Python 3
* Youtube API client
* Pillow
### Python 2.7
* Youtube API client
* oauth2client
## Setup
* Create an API application: https://console.cloud.google.com/apis/api/youtube.googleapis.com/
* Download your client-secret.json file
* Add your client secret to the directory where SubBanner is installed
* add the path to your client secret in banner.py
* Add your YouTube Channel ID at the bottom of banner.py
* Run banner.py with `python3 banner.py`
