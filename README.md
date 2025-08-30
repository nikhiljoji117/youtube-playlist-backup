# YouTube Playlist Backup  
A Python tool to backup YouTube playlists into structured Excel files using the YouTube Data API.  

## About this project  
This script connects to your YouTube account via **OAuth 2.0**, fetches all your playlists (including private), and saves them into a single Excel workbook.  
Each playlist is exported to its **own sheet**, with videos sorted from oldest to newest.  
At the end of 2024 there was a bug in Youtube where many accounts including mine were flagged and all the playlist was lost. Although it was fixed a few hours later, I really want to avoid that and is the main reason for making this.

---

## Features  
- Accesses **public, unlisted, and private playlists**  
- Exports video details:  
  - Title  
  - Channel Name  
  - Video URL  
  - Date Added  
- Each playlist saved in a **separate Excel sheet**  
- Videos sorted **chronologically** (oldest first)  

---

## Setup & Usage  
1. Clone or download this repository  
2. Download your `client_secret.json` from Google Cloud (OAuth Client ID – Desktop App) and place it in the same folder as `script_oauth.py`. This file is required for authentication but must be kept private and never uploaded to GitHub.
