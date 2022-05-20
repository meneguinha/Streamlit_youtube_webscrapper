import streamlit as st
import pandas as pd
import xlsxwriter
from pytube import extract
from apiclient.discovery import build
from modules.yt_functions import get_channel_videos, scrape_comments_with_replies, to_excel

st.image("mining.png")
st.title("YouTube Web Scrapper")
st.text("With this simple app you can get comments on videos in any channel on Youtube.\nYou just need a Youtube API Key.")
st.text("To get this key, you just nedd to follow simple steps \nin the Google Cloud Plataform.\nTo create it, follow the video tutorial.")
st.video("tutorial.mp4")
st.subheader("Set up your API KEY")
api_key = st.text_input(label="Your YouTube API KEY", value="", help = "If you don't have one, create on cloude.google.com")
st.subheader("Wich channel user do you want to analyze?")
st.write("To get channel user from a channel url:")
st.markdown("https://commentpicker.com/youtube-channel-id.php#find-youtube-channel-url")
yt_channel = st.text_input(label="Channel User (not channel url)", value="")

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
    st.write("Total number of videos:", qt_videos)
    
    finish_val = int(finish_val)
    if finish_val>qt_videos:
        finish_val=qt_videos

    list_of_ids = df.VideoId[0:finish_val].values.tolist()
    
    
    box = [['Name', 'Comment', 'Time', 'Likes', 'Reply Count']]
    
    for video_id in list_of_ids:
        aux_df = scrape_comments_with_replies(video_id, api_key)
    test_df = aux_df.astype(str)
    test_df=test_df.replace('\\n','',regex=True)
    st.dataframe(test_df)
    df_xlsx = to_excel(test_df)
    st.download_button(label='Download Current Result', data=df_xlsx, file_name= 'data_extracted.xlsx')  
    