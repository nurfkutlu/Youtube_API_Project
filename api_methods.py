import pandas as pd

# Method 1 :

def get_channel_stats(youtube, channel_ids):
    all_data = []

    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=",".join(channel_ids)
    )

    response = request.execute()

    # loop through items in response
    for item in response["items"]:
        data = {'channelName': item['snippet']['title'],
                'subscribers': item['statistics']['subscriberCount'],
                'views': item['statistics']['viewCount'],
                'totalVideos': item['statistics']['videoCount'],
                'playlistId': item['contentDetails']['relatedPlaylists']['uploads']
        }
        all_data.append(data)
    
    return pd.DataFrame(all_data)
"""
---------------------------------------------------------
"""
# method 2

def get_video_ids(youtube, playlist_id):
    video_ids = []

    request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=playlist_id,
            maxResults=50
        )
    response = request.execute()

    for item in response['items']:
        video_ids.append(item['contentDetails']['videoId'])

    next_page_token = response.get('nextPageToken')
    
    while next_page_token is not None:
        request = youtube.playlistItems().list(
                part="snippet,contentDetails",
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token
            )
        response = request.execute()

        for item in response['items']:
            video_ids.append(item['contentDetails']['videoId'])

        next_page_token = response.get('nextPageToken')    

        
    return video_ids

"""
---------------------------------------------------------
"""
#Method 3 

def get_most_pop_Youtube_TR(youtube):
    all_data = []

# This request method is defined as below . You can include what you want in part. 
    # https://developers.google.com/youtube/v3/docs/channels/list#usage you can look detailly.
    
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        chart="mostPopular",
        regionCode="TR",
    )
    response = request.execute()


    # loop through items in response
    #json webpage ( https://jsonformatter.org/json-editor) is sooo good to anayze.
    for item in response["items"]:
        data = {'channelName': item['snippet']['title'],
                'PublishTime': item['snippet']['publishedAt'],
                'views': item['statistics']['viewCount'],
                'LikeCount':item['statistics']['likeCount'],
                'CommentCount':item['statistics']['commentCount'],
                'Duration': item['contentDetails']['duration'],
                'videoID': item['id']
        }
        all_data.append(data)

        """ 
        ------------------------------------------------------
        
        """

# Get comments for the specified video
comments = []
nextPageToken = None

while True:
    request = youtube.commentThreads().list(
        part="snippet",
        videoId="5nXRi1dkRps",
        maxResults=500,  # Adjust as needed
        pageToken=nextPageToken
    )
    response = request.execute()

    for item in response["items"]:
        comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        comments.append(comment)

    nextPageToken = response.get("nextPageToken")

    if not nextPageToken:
        break

# Print or use the retrieved comments
for comment in comments:
    print(comment)