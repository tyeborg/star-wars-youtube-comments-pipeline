# pip install google-api-python-client==2.86.0
import pandas as pd
from dateutil import parser
from googleapiclient.discovery import build

class Extract():
    def __init__(self):
        # Initialize variables.
        self.api_service_name = 'youtube'
        self.api_version = 'v3'
        self.api_key = 'AIzaSyBfsz13OHhGI51aPMASG4NtfmM4EBbWyDY'
        
        # @starwars YouTube channel ID.
        self.channel_id = 'UCZGYJFUizSax-yElQaFDp5Q' 
        self.youtube = build(self.api_service_name, self.api_version, developerKey=self.api_key)
    
    def get_channel_info(self):
        # Get the channel information
        channel_response = self.youtube.channels().list(
            part='snippet',
            id=self.channel_id
        )
        channel_response = channel_response.execute()
        
        return(channel_response)
    
    def get_videos_list(self):
        # Receive @starwars channel info.
        channel_response = self.get_channel_info()
        
        # Extract the channel creation date
        channel_created = channel_response['items'][0]['snippet']['publishedAt']
        channel_created_date = parser.parse(channel_created)
        
        # Define the search query parameters
        # Find videos that contain 'Trailer'.
        query = 'Trailer'
        # Number of videos to retrieve per code execution.
        num_results = 5 
        # All videos published after @starwars' YouTube channel conception.
        published_after = channel_created_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        
        # Call the YouTube Data API to retrieve the list of videos.
        search_response = self.youtube.search().list(
            part='id,snippet',
            channelId=self.channel_id,
            q=query,
            type='video',
            maxResults=num_results,
            publishedAfter=published_after
        )
        search_response = search_response.execute()
        
        return(search_response)
    
    def get_comments(self, comments_list):
        videos_info_list = self.get_videos_list()
        
        # Extract the video ids and titles from the API response
        video_ids = []
        video_titles = []
        for info in videos_info_list.get('items', []):
            video_ids.append(info['id']['videoId'])
            video_titles.append(info['snippet']['title'])
            
        print(video_titles)
        
        # Initialize a list to store the comment data.
        #comments = []
           
        try:
            # Initialize a counter.
            counter1 = 0

            # Call the YouTube Data API to retrieve comments for the videos.
            for video_id, video_title in zip(video_ids, video_titles):
                results = self.youtube.commentThreads().list(
                    part='snippet',
                    videoId=video_id,
                    textFormat='plainText',
                    maxResults=200
                )
                results = results.execute()
                
                counter1 += 1
                counter2 = 0
                
                while results and counter2 < 200:
                    for item in results['items']:
                        star_wars_comment = {
                            'comment_id': item['snippet']['topLevelComment']['id'],
                            'video_title': video_title,
                            'author': item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                            'comment': item['snippet']['topLevelComment']['snippet']['textDisplay'],
                            'date': item['snippet']['topLevelComment']['snippet']['publishedAt'],
                            'sentiment': '' 
                        }
                        comments_list.append(star_wars_comment)

                        counter2 += 1
                        if counter2 == 200:
                            break
                        
                    if counter2 == 200:
                        break
    
                if counter1 == 1000:
                    break
                
            print("[+] Data successfully extracted using YouTube API v3")
            
        except(Exception) as error:
            print("[-] Data failed to extract using YouTube API v3:", error)
                
        # Return comments list.
        return(comments_list)