import streamlit as st
import cv2
import tempfile
import numpy as np
from collections import defaultdict
import pandas as pd

from quadrant_balls import detect_balls, update_trackers, check_events, get_quadrant

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    
    frame_count = 0
    ball_trackers = defaultdict(lambda: defaultdict(dict))
    events = []

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    progress_bar = st.progress(0)
    status_text = st.empty()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_count += 1
        
        progress_bar.progress(frame_count / total_frames)
        status_text.text(f"Processing frame {frame_count}/{total_frames}")
        
        try:
            balls = detect_balls(frame)
            update_trackers(ball_trackers, balls, frame_count)
            new_events = check_events(ball_trackers, frame_count)
            events.extend(new_events)
        except Exception as e:
            st.error(f"Error processing frame {frame_count}: {str(e)}")
            st.error(f"Trackers state: {ball_trackers}")
            break  # Stop processing if an error occurs
        
    cap.release()
    return events

st.title('QuadBall Tracker 🔴🟢🔵🟡')

st.write("""
Welcome to QuadBall Tracker! This application uses computer vision to track colored balls 
across different quadrants in a video. Upload your video to get started!
""")

uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "avi", "mov"])

if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False) 
    tfile.write(uploaded_file.read())
    
    st.video(tfile.name)
    
    if st.button('Process Video'):
        events = process_video(tfile.name)
        
        st.success('Video processing complete!')
        
        st.subheader('Event Log')
        for event in events:
            st.write(f"Time: {event['time']}, Quadrant: {event['quadrant']}, "
                     f"Color: {event['color']}, Type: {event['type']}")
        
        # Create a DataFrame for easy filtering
        df = pd.DataFrame(events)
        
        st.subheader('Filter Events')
        color_filter = st.multiselect('Select colors', df['color'].unique())
        quadrant_filter = st.multiselect('Select quadrants', df['quadrant'].unique())
        
        filtered_df = df
        if color_filter:
            filtered_df = filtered_df[filtered_df['color'].isin(color_filter)]
        if quadrant_filter:
            filtered_df = filtered_df[filtered_df['quadrant'].isin(quadrant_filter)]
        
        st.dataframe(filtered_df)

st.sidebar.title('About')
st.sidebar.info('This application uses computer vision to track colored balls across video quadrants. '
                'Upload a video to see it in action!')