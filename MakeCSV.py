import Secret   # Used to import private api credentials from config file
import tweepy   # Third party python library used to interact with twitter api
import os       # Handles creation and naming of paths and files
import time     # Used to get current unix timestamp for use in the csv filename
import csv      # Used to write the response to csv

### Instantiate tweepy authentication handler by passing in API credentials
auth = tweepy.OAuth1UserHandler(
    Secret.apikey, 
    Secret.apikeysecret, 
    Secret.accesstoken, 
    Secret.accesstokensecret)

### Instantiate tweepy API object by passing in the previously made authentication handler
api = tweepy.API(
    auth,
    wait_on_rate_limit=True
    )

### Self explanatory
myUserName = input('What is the username of the account whose liked tweets you wish to view? ')

### Create path to a directory called LIKEDTWEETS
userFolder = os.path.join(os.getcwd(),'LIKEDTWEETS')
if not os.path.exists(userFolder):
    os.makedirs(userFolder)

### Create filename for the csv that will be saved into LIKEDTWEETS
filename= myUserName +"-"+ str(time.time()).split('.')[0]+'.csv' 
fullpath = os.path.join(userFolder,filename)

### Ping the API for the user's liked tweets, parsing the json response for key info : [NAME, USERNAME, TWEET_TEXT, TIMESTAMP, FAVORITE_COUNT]
### Write each row into a csv
with open(fullpath,'w+') as liked:
    a=csv.writer(liked)
    for page in tweepy.Cursor(api.get_favorites, screen_name=myUserName,tweet_mode='extended').pages():
        for tweet in page:
            a.writerow([
                tweet._json['user']['name'],
                tweet._json['user']['screen_name'],
                tweet._json['full_text'],
                tweet.created_at,
                tweet._json['favorite_count']
                ])

