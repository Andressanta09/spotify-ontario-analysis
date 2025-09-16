import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from datetime import datetime

# Load data
with open('data.json', 'r') as f:
    data = json.load(f)

# Set page config
st.set_page_config(
    page_title="Ontario Music Analysis",
    page_icon="🎵",
    layout="wide"
)

# Title and description
st.title("🎵 Ontario Music Analysis Dashboard")
st.markdown("""
This dashboard presents an analysis of music trends from Spotify playlists in Ontario.
Explore the characteristics and patterns of music popular in the region.
""")

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Overview", "Temporal Analysis", "Track Analysis"])

if page == "Overview":
    # Display key metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Tracks Analyzed", len(data['top_tracks']))
    with col2:
        avg_popularity = sum(track['popularity'] for track in data['top_tracks']) / len(data['top_tracks'])
        st.metric("Average Track Popularity", f"{avg_popularity:.1f}")
    with col3:
        latest_year = max(int(track['release_date'][:4]) for track in data['top_tracks'])
        st.metric("Latest Year", str(latest_year))
    
    # Feature correlations heatmap
    st.header("Feature Correlations")
    corr_df = pd.DataFrame(data['feature_correlations'])
    fig = px.imshow(corr_df, 
                    labels=dict(color="Correlation"),
                    color_continuous_scale="RdBu")
    st.plotly_chart(fig, use_container_width=True)

elif page == "Temporal Analysis":
    st.header("Music Trends Over Time")
    
    # Convert yearly trends to DataFrame
    yearly_df = pd.DataFrame(data['yearly_trends'])
    
    # Feature selector
    features = ['danceability', 'energy', 'valence', 'popularity']
    selected_features = st.multiselect(
        "Select features to display",
        features,
        default=['danceability', 'energy']
    )
    
    if selected_features:
        fig = go.Figure()
        for feature in selected_features:
            fig.add_trace(go.Scatter(
                x=yearly_df['release_year'],
                y=yearly_df[feature],
                name=feature,
                mode='lines+markers'
            ))
        fig.update_layout(
            title='Feature Trends Over Time',
            xaxis_title='Year',
            yaxis_title='Value'
        )
        st.plotly_chart(fig, use_container_width=True)

else:  # Track Analysis
    st.header("Track Analysis")
    
    # Convert top tracks to DataFrame
    tracks_df = pd.DataFrame(data['top_tracks'])
    
    # Top tracks table
    st.subheader("Top Tracks by Popularity")
    st.dataframe(
        tracks_df[['name', 'artist', 'album', 'popularity']]
        .sort_values('popularity', ascending=False)
        .reset_index(drop=True)
    )
    
    # Feature distribution
    st.subheader("Feature Distributions")
    feature = st.selectbox(
        "Select feature to visualize",
        ['danceability', 'energy', 'valence', 'popularity']
    )
    
    fig = px.histogram(tracks_df, x=feature)
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Data last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))