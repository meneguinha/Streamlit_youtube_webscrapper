import streamlit as st
import pandas as pd
from pytube import extract
from apiclient.discovery import build
from modules.yt_functions import get_channel_videos, scrape_comments_with_replies
import time
st.title("YouTube Web Scrapper")
st.text("With this simple app you can get all comments from any channel on Youtube. You just need a Youtube API Key.")
st.text("To get this key, you just nedd to follow simple steps in the Google Cloud Plataform")
st.image("gif1.gif")
st.image("gif2.gif")
api_key = st.text_input(label="Your YouTube API KEY", value="", help = "If you don't have one, create on cloude.google.com")
st.write("Extract YouTube Comments from a list of Videos")

yt_channel = st.text_input(label="Channel User.", value="")
finish_val = st.text_input(label="Number of most recent videos you want to analyze", value="")
startprocess = st.button(label = "Start Scraping",)

if startprocess:
    api_key = str(api_key)
    yt_channel = str(yt_channel)
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    videos = get_channel_videos(yt_channel, api_key)
    
    list = []
    for video in videos:
        a = video['snippet']['publishedAt']
        b = video['snippet']['title']
        c = video['snippet']['resourceId']['videoId']
        aux_list = [a,b,c]
        list.append(aux_list)
    df = pd.DataFrame(list, columns = ['Date', 'Title','VideoId'])
    
    qt_videos = len(videos)
    st.write("There is a total of", qt_videos)
    
    finish_val = int(finish_val)
    if finish_val>qt_videos:
        finish_val=qt_videos

    list_of_ids = df.VideoId[0:10].values.tolist()
    
    
    box = [['Name', 'Comment', 'Time', 'Likes', 'Reply Count']]
    
    for video_id in list_of_ids:
        aux_df = scrape_comments_with_replies(video_id, api_key)
    test_df = aux_df.astype(str)
    test_df=test_df.replace('\\n','',regex=True)
    st.dataframe(test_df)
    csv = df.to_csv(encoding='utf-8', errors="ignore")
    st.download_button("Press to Download", csv,  "file.csv", "text/csv",   key='download-csv')