from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import subprocess
import pickle

CLIENT_SECRET_FILE = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_KEY = 'your key here'
command = "python2 bannerupdate.py --file banner.png" #dont change this unless you want it to break

print("Process started.")  # Add this line


def get_authenticated_service():
    try:
        with open('credentials.pkl', 'rb') as token:
            credentials = pickle.load(token)
    except FileNotFoundError:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
        credentials = flow.run_local_server()
        with open('credentials.pkl', 'wb') as token:
            pickle.dump(credentials, token)

    return build('youtube', 'v3', credentials=credentials, developerKey=API_KEY)


def get_subscriber_count(youtube, channel_id):
  request = youtube.channels().list(part="statistics", id=channel_id)
  response = request.execute()
  print("Response: ", response)  # Add this line
  return response['items'][0]['statistics']['subscriberCount']


from PIL import Image, ImageDraw, ImageFont


def create_banner(subscriber_count):
  img = Image.new('RGB', (2560, 1440), color=(90,4,199))
  d = ImageDraw.Draw(img)
  fnt = ImageFont.truetype(
      'font.ttf', 150)
  fnt2 = ImageFont.truetype(
      'font.ttf', 32)
  d.text((730, 599),
         f"{subscriber_count} subscribers",
         font=fnt,
         fill=(255, 255, 255))
  d.text((1024, 825),
         f"updated every 8 minutes",
         font=fnt2,
         fill=(255, 255, 255))
  img.save('banner.png')


def upload_banner(youtube, banner_file, channel_id):
  # Upload the banner image to YouTube
  media = MediaFileUpload(banner_file, mimetype='image/png', resumable=True)
  response = youtube.channelBanners().insert(
    media_body=media,
    body={'channelId': channel_id}
  ).execute()

  # Update the channel's branding settings to use the new banner
  channels_update_response = youtube.channels().update(
      part='id,brandingSettings',
      body={
          'id': channel_id,
          'brandingSettings': {
            'channel': {
                'defaultTab': 'home'
            },
              'image': {
                  'bannerExternalUrl': response['url']
              }
          }
      }).execute()
  print("Channel Update Response: ", channels_update_response)  # Add this line
# Assuming you have the necessary channel ID and banner file path
channel_id = 'put your channel id here'
banner_file_path = 'banner.png'

# Getting authenticated service
youtube = get_authenticated_service()

# Getting subscriber count
subscriber_count = get_subscriber_count(youtube, channel_id)

# Creating a banner
create_banner(subscriber_count)

# Uploading the banner

subprocess.run(command, shell=True)