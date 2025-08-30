import os
import pandas as pd
import re
from datetime import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import pickle

# Scopes for read-only access
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]

# Authenticate user via OAuth
def authenticate():
    creds = None
    # Load token if exists
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    # If token is expired or missing, log in again
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("youtube", "v3", credentials=creds)

# Get all playlists for the logged-in user
def get_playlists(youtube):
    playlists = []
    next_page_token = None

    while True:
        request = youtube.playlists().list(
            part="snippet",
            mine=True,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()
        playlists.extend(response["items"])
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return playlists

# Get all videos from a playlist
def get_videos_from_playlist(youtube, playlist_id):
    videos = []
    next_page_token = None

    while True:
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()
        videos.extend(response["items"])
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return videos

# Excel sheet name cleaner
def clean_sheet_name(name):
    return re.sub(r"[\\/*?:\[\]]", "", name)[:31]

# Write playlists to Excel
def backup_to_excel(youtube, playlists):
    with pd.ExcelWriter("youtube_playlists_oauth.xlsx", engine="openpyxl") as writer:
        for playlist in playlists:
            title = playlist["snippet"]["title"]
            playlist_id = playlist["id"]
            print(f"Processing: {title}")
            videos = get_videos_from_playlist(youtube, playlist_id)
            video_data = []

            for item in videos:
                snippet = item["snippet"]
                video_data.append({
                    "Video Title": snippet.get("title"),
                    "Channel Name": snippet.get("videoOwnerChannelTitle"),
                    "Video URL": f"https://www.youtube.com/watch?v={snippet.get('resourceId', {}).get('videoId')}",
                    "Date Added": snippet.get("publishedAt")
                })

            df = pd.DataFrame(video_data)
            df["Date Added"] = pd.to_datetime(df["Date Added"]).dt.tz_localize(None)
            df.sort_values("Date Added", inplace=True)

            sheet_name = clean_sheet_name(title)
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    print("Backup complete! Saved as 'youtube_playlists_oauth.xlsx'.")

# Run the flow
if __name__ == "__main__":
    print("Authenticating via OAuth...")
    yt = authenticate()
    print("Fetching your playlists...")
    playlists = get_playlists(yt)
    if playlists:
        backup_to_excel(yt, playlists)
    else:
        print("No playlists found.")
