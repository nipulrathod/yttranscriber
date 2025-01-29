import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import os 
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

prompt = """You are Yotube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here:  """

def extract_video_id(youtube_url):
    parsed_url = urlparse(youtube_url)
    query_params = parse_qs(parsed_url.query)
    return query_params.get("v", [None])[0]

def extract_transcript_details(youtube_video_url):
    try:
        # video_id=youtube_video_url.split("=")[1]
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)
        
        transcript = ""
        for i in transcript_text:
            transcript +=  " " + i["text"]
            
        return transcript
    
    except Exception as e:
        raise e
def generate_gemini_content(transcript_text,prompt):
    
    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)
    return response.text

st.title("Youtube Transcript to Detailed Note Converter")
youtube_link = st.text_input("Enter Youtube Video Link:")

if youtube_link:
    video_id = extract_video_id(youtube_link)
    
    if video_id:
        st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)
    else:
        st.error("Invalid YouTube URL. Please check the link.")    
    # video_id = youtube_link.split("=")[1]
    
    
if st.button("Get Detailed Notes"):
    video_id = extract_video_id(youtube_link)
    
    if video_id:
        transcript_text = extract_transcript_details(video_id)
        if transcript_text:
            summary = generate_gemini_content(transcript_text, prompt)
            st.markdown("## Detailed Notes:")
            st.write(summary)
        else:
            st.error("No transcript available for this video.")
    else:
        st.error("Invalid YouTube URL. Please check the link.")