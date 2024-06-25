from googleapiclient.discovery import build
from pymango import MangoClient
import json

def get_youtube_service(api_key):
    """Builds and returns the YouTube service object."""
    youtube = build('youtube', 'v3', developerKey=api_key)
    return youtube

def getYoutubeTrendVids(youtube_service):
    """Retrieve trending videos in Morocco."""
    request = youtube_service.videos().list(
        maxResults=10,
        part="snippet,contentDetails",
        chart="mostPopular",
        type="video",
        regionCode="MA"
    )
    trendvids = request.execute()
    return trendvids['items']

def getVideocomment(youtube_service, videoid):
    """Retrieve comments for a given video."""
    comments = []
    request = youtube_service.commentThreads().list(
        part="snippet",
        videoId=videoid
    )
    videos_comments = request.execute()

    for item in videos_comments['items']:
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
        comments.append(comment)
    
    return comments

def vids_comments_details(youtube_service):
    """Retrieve details and comments for trending videos."""
    data_storage = []
    videos = getYoutubeTrendVids(youtube_service)

    for video in videos:
        video_id = video['id']
        video_title = video['snippet']['title']
        comments = getVideocomment(youtube_service, video_id)
        
        video_data = {
            "video_details": {
                "id": video_id,
                "title": video_title,
                "snippet": video['snippet'],  # Entire snippet for more details if needed
                "contentDetails": video['contentDetails']  # Content details if needed
            },
            "comments": comments
        }
        
        data_storage.append(video_data)
    
    return data_storage

    #Store data in MongoDB.
    def mangodb_storage(data, db_name ="youtubevidsdetails", collection_name="trending_videos"):
        client = MongoClient('localhost', 27017)  # Adjust the host and port as necessary
        db = client[db_name]
        collection = db[collection_name]
        collection.insert_many(data)
        print("Data successfully inserted into MongoDB.")

if __name__ == "__main__":
    # Define your API key
    api_key = 'AIzaSyBgoc2NaDTK4OlKQwG5O8zx1QeYdD1nW24'

    # Get the YouTube service
    youtube_service = get_youtube_service(api_key)

    # Retrieve and store videos with their comments and details
    video_data_storage = vids_comments_details(youtube_service)

    #store the data of the videos inn the mango database
    mangodb_storage(video_data_storage)
