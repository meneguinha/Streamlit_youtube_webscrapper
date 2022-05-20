from apiclient.discovery import build
import pandas as pd
#Get All Channel Videos

def get_channel_videos(channel_id, api_key2):
        youtube = build('youtube', 'v3', developerKey=api_key2)
        # get Uploads playlist id
        res = youtube.channels().list(id=channel_id, 
                                    part='contentDetails').execute()
        playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        
        videos = []
        next_page_token = None
        
        while 1:
            res = youtube.playlistItems().list(playlistId=playlist_id, 
                                            part='snippet', 
                                            maxResults=50,
                                            pageToken=next_page_token).execute()
            videos += res['items']
            next_page_token = res.get('nextPageToken')
            
            if next_page_token is None:
                break
        
        return videos

def scrape_comments_with_replies(video_id,api_key2):
        box = [['Name', 'Comment', 'Time', 'Likes', 'Reply Count']]
        youtube = build('youtube', 'v3', developerKey=api_key2)
        data = youtube.commentThreads().list(part='snippet', videoId=video_id, maxResults='100', textFormat="plainText").execute()

        for i in data["items"]:

            name = i["snippet"]['topLevelComment']["snippet"]["authorDisplayName"]
            comment = i["snippet"]['topLevelComment']["snippet"]["textDisplay"]
            published_at = i["snippet"]['topLevelComment']["snippet"]['publishedAt']
            likes = i["snippet"]['topLevelComment']["snippet"]['likeCount']
            replies = i["snippet"]['totalReplyCount']

            box.append([name, comment, published_at, likes, replies])

            totalReplyCount = i["snippet"]['totalReplyCount']

            if totalReplyCount > 0:

                parent = i["snippet"]['topLevelComment']["id"]

                data2 = youtube.comments().list(part='snippet', maxResults='100', parentId=parent,
                                                textFormat="plainText").execute()

                for i in data2["items"]:
                    name = i["snippet"]["authorDisplayName"]
                    comment = i["snippet"]["textDisplay"]
                    published_at = i["snippet"]['publishedAt']
                    likes = i["snippet"]['likeCount']
                    replies = ""

                    box.append([name, comment, published_at, likes, replies])

        while ("nextPageToken" in data):

            data = youtube.commentThreads().list(part='snippet', videoId=ID, pageToken=data["nextPageToken"],
                                                maxResults='100', textFormat="plainText").execute()

            for i in data["items"]:
                name = i["snippet"]['topLevelComment']["snippet"]["authorDisplayName"]
                comment = i["snippet"]['topLevelComment']["snippet"]["textDisplay"]
                published_at = i["snippet"]['topLevelComment']["snippet"]['publishedAt']
                likes = i["snippet"]['topLevelComment']["snippet"]['likeCount']
                replies = i["snippet"]['totalReplyCount']

                box.append([name, comment, published_at, likes, replies])

                totalReplyCount = i["snippet"]['totalReplyCount']

                if totalReplyCount > 0:

                    parent = i["snippet"]['topLevelComment']["id"]

                    data2 = youtube.comments().list(part='snippet', maxResults='100', parentId=parent,
                                                    textFormat="plainText").execute()

                    for i in data2["items"]:
                        name = i["snippet"]["authorDisplayName"]
                        comment = i["snippet"]["textDisplay"]
                        published_at = i["snippet"]['publishedAt']
                        likes = i["snippet"]['likeCount']
                        replies = ''

                        box.append([name, comment, published_at, likes, replies])

        new_df = pd.DataFrame({'Name': [i[0] for i in box], 'Comment': [i[1] for i in box], 'Time': [i[2] for i in box],
                        'Likes': [i[3] for i in box], 'Reply Count': [i[4] for i in box]})


        return new_df
