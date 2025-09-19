"""
Spotify Ontario Analysis - Automated Report Generator

This script generates comprehensive HTML reports from the processed data.
Reports include visualizations, statistics, and insights.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
import glob
import os
from datetime import datetime
import json
from pathlib import Path


class ReportGenerator:
    """Generate automated analysis reports."""
    
    def __init__(self, data_dir="../data/processed", output_dir="../reports"):
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Load data
        self.tracks_df = None
        self.playlists_df = None
        self.load_data()
        
    def load_data(self):
        """Load the most recent processed data files."""
        try:
            # Find most recent files
            track_patterns = [
                f"{self.data_dir}/clean_tracks_*.parquet",
                f"{self.data_dir}/clean_tracks_*.csv"
            ]
            
            playlist_patterns = [
                f"{self.data_dir}/clean_playlists_*.parquet",
                f"{self.data_dir}/clean_playlists_*.csv"
            ]
            
            # Load tracks
            for pattern in track_patterns:
                files = glob.glob(str(pattern))
                if files:
                    latest_file = max(files, key=os.path.getctime)
                    if latest_file.endswith('.parquet'):
                        self.tracks_df = pd.read_parquet(latest_file)
                    else:
                        self.tracks_df = pd.read_csv(latest_file)
                    print(f"✅ Loaded tracks data: {latest_file}")
                    break
            
            # Load playlists
            for pattern in playlist_patterns:
                files = glob.glob(str(pattern))
                if files:
                    latest_file = max(files, key=os.path.getctime)
                    if latest_file.endswith('.parquet'):
                        self.playlists_df = pd.read_parquet(latest_file)
                    else:
                        self.playlists_df = pd.read_csv(latest_file)
                    print(f"✅ Loaded playlists data: {latest_file}")
                    break
            
            if self.tracks_df is None:
                raise FileNotFoundError("No processed tracks data found")
                
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            raise
    
    def create_summary_stats(self):
        """Generate summary statistics."""
        stats = {
            'total_tracks': len(self.tracks_df),
            'total_playlists': len(self.playlists_df) if self.playlists_df is not None else 0,
            'unique_artists': self.tracks_df['artist'].nunique() if 'artist' in self.tracks_df.columns else 0,
            'unique_albums': self.tracks_df['album'].nunique() if 'album' in self.tracks_df.columns else 0
        }
        
        # Date range
        if 'release_date' in self.tracks_df.columns:
            try:
                self.tracks_df['release_year'] = pd.to_datetime(self.tracks_df['release_date'], errors='coerce').dt.year
                stats['year_range'] = {
                    'min': int(self.tracks_df['release_year'].min()),
                    'max': int(self.tracks_df['release_year'].max())
                }
            except:
                stats['year_range'] = None
        
        return stats
    
    def create_popularity_chart(self):
        """Create popularity distribution chart."""
        if 'popularity' not in self.tracks_df.columns:
            return None
            
        fig = px.histogram(
            self.tracks_df, 
            x='popularity',
            nbins=20,
            title="Track Popularity Distribution",
            labels={'popularity': 'Popularity Score', 'count': 'Number of Tracks'},
            color_discrete_sequence=['#1DB954']
        )
        
        fig.update_layout(
            title_x=0.5,
            height=400,
            showlegend=False
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def create_audio_features_radar(self):
        """Create radar chart for average audio features."""
        audio_features = ['danceability', 'energy', 'valence', 'acousticness', 
                         'instrumentalness', 'liveness', 'speechiness']
        
        available_features = [f for f in audio_features if f in self.tracks_df.columns]
        
        if not available_features:
            return None
        
        # Calculate means
        means = self.tracks_df[available_features].mean()
        
        # Create radar chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=means.values,
            theta=[f.title() for f in available_features],
            fill='toself',
            name='Average Audio Features',
            line_color='#1DB954'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )),
            showlegend=True,
            title="Average Audio Features Profile",
            title_x=0.5,
            height=500
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def create_yearly_trends(self):
        """Create yearly trends chart."""
        if 'release_year' not in self.tracks_df.columns:
            return None
        
        audio_features = ['danceability', 'energy', 'valence']
        available_features = [f for f in audio_features if f in self.tracks_df.columns]
        
        if not available_features:
            return None
        
        # Group by year and calculate means
        yearly_trends = self.tracks_df.groupby('release_year')[available_features].mean().reset_index()
        
        # Filter reasonable years
        yearly_trends = yearly_trends[
            (yearly_trends['release_year'] >= 1990) & 
            (yearly_trends['release_year'] <= 2025)
        ]
        
        fig = go.Figure()
        colors = ['#1DB954', '#1ed760', '#00d461']
        
        for i, feature in enumerate(available_features):
            fig.add_trace(go.Scatter(
                x=yearly_trends['release_year'],
                y=yearly_trends[feature],
                mode='lines+markers',
                name=feature.title(),
                line=dict(color=colors[i % len(colors)], width=3),
                marker=dict(size=6)
            ))
        
        fig.update_layout(
            title="Audio Features Trends Over Time",
            title_x=0.5,
            xaxis_title="Year",
            yaxis_title="Feature Value",
            height=400,
            hovermode='x unified'
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def create_top_artists_chart(self):
        """Create top artists chart."""
        if 'artist' not in self.tracks_df.columns:
            return None
        
        # Count tracks per artist
        artist_counts = self.tracks_df['artist'].value_counts().head(15)
        
        fig = px.bar(
            x=artist_counts.values,
            y=artist_counts.index,
            orientation='h',
            title="Top 15 Artists by Track Count",
            labels={'x': 'Number of Tracks', 'y': 'Artist'},
            color=artist_counts.values,
            color_continuous_scale='Viridis'
        )
        
        fig.update_layout(
            title_x=0.5,
            height=500,
            yaxis={'categoryorder': 'total ascending'},
            showlegend=False
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def create_correlation_heatmap(self):
        """Create audio features correlation heatmap."""
        audio_features = ['danceability', 'energy', 'valence', 'tempo', 'loudness',
                         'acousticness', 'instrumentalness', 'liveness', 'speechiness']
        
        available_features = [f for f in audio_features if f in self.tracks_df.columns]
        
        if len(available_features) < 2:
            return None
        
        # Calculate correlation matrix
        corr_matrix = self.tracks_df[available_features].corr()
        
        fig = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="RdBu_r",
            title="Audio Features Correlation Matrix"
        )
        
        fig.update_layout(
            title_x=0.5,
            height=600
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def generate_html_report(self):
        """Generate complete HTML report."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Generate components
        stats = self.create_summary_stats()
        popularity_chart = self.create_popularity_chart()
        radar_chart = self.create_audio_features_radar()
        trends_chart = self.create_yearly_trends()
        artists_chart = self.create_top_artists_chart()
        correlation_chart = self.create_correlation_heatmap()
        
        # Build HTML report
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Spotify Ontario Analysis Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f8f9fa;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            margin-bottom: 40px;
            border-bottom: 3px solid #1DB954;
            padding-bottom: 20px;
        }}
        .header h1 {{
            color: #1DB954;
            font-size: 2.5rem;
            margin: 0;
        }}
        .header p {{
            color: #666;
            font-size: 1.1rem;
            margin: 10px 0 0 0;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        .stat-card {{
            background: linear-gradient(135deg, #1DB954, #1ed760);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(29, 185, 84, 0.3);
        }}
        .stat-card h3 {{
            margin: 0 0 10px 0;
            font-size: 2rem;
        }}
        .stat-card p {{
            margin: 0;
            opacity: 0.9;
        }}
        .section {{
            margin: 40px 0;
        }}
        .section h2 {{
            color: #2c3e50;
            border-bottom: 2px solid #1DB954;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        .chart-container {{
            margin: 20px 0;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .footer {{
            text-align: center;
            margin-top: 50px;
            padding-top: 20px;
            border-top: 2px solid #1DB954;
            color: #666;
        }}
        .no-data {{
            text-align: center;
            color: #666;
            font-style: italic;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>🎵 Spotify Ontario Analysis Report</h1>
            <p>Comprehensive analysis of Ontario music data from Spotify</p>
            <p><strong>Generated:</strong> {datetime.now().strftime("%B %d, %Y at %H:%M")}</p>
        </header>
        
        <section class="section">
            <h2>📊 Summary Statistics</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <h3>{stats['total_tracks']:,}</h3>
                    <p>Total Tracks</p>
                </div>
                <div class="stat-card">
                    <h3>{stats['total_playlists']:,}</h3>
                    <p>Playlists Analyzed</p>
                </div>
                <div class="stat-card">
                    <h3>{stats['unique_artists']:,}</h3>
                    <p>Unique Artists</p>
                </div>
                <div class="stat-card">
                    <h3>{stats['unique_albums']:,}</h3>
                    <p>Unique Albums</p>
                </div>
            </div>
        </section>
        
        <section class="section">
            <h2>📈 Track Popularity Distribution</h2>
            <div class="chart-container">
                {popularity_chart if popularity_chart else '<div class="no-data">Popularity data not available</div>'}
            </div>
        </section>
        
        <section class="section">
            <h2>🎼 Audio Features Profile</h2>
            <div class="chart-container">
                {radar_chart if radar_chart else '<div class="no-data">Audio features data not available</div>'}
            </div>
        </section>
        
        <section class="section">
            <h2>🎤 Top Artists</h2>
            <div class="chart-container">
                {artists_chart if artists_chart else '<div class="no-data">Artist data not available</div>'}
            </div>
        </section>
        
        <section class="section">
            <h2>📅 Musical Trends Over Time</h2>
            <div class="chart-container">
                {trends_chart if trends_chart else '<div class="no-data">Temporal data not available</div>'}
            </div>
        </section>
        
        <section class="section">
            <h2>🔗 Audio Features Correlations</h2>
            <div class="chart-container">
                {correlation_chart if correlation_chart else '<div class="no-data">Correlation data not available</div>'}
            </div>
        </section>
        
        <footer class="footer">
            <p>Report generated by Spotify Ontario Analysis System</p>
            <p>Data processed on {datetime.now().strftime("%Y-%m-%d")}</p>
        </footer>
    </div>
</body>
</html>
"""
        
        # Save report
        report_path = self.output_dir / f"ontario_music_analysis_report_{timestamp}.html"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Report generated: {report_path}")
        return report_path


def main():
    """Main function to generate reports."""
    print("🎵 Spotify Ontario Analysis - Report Generator")
    print("=" * 50)
    
    try:
        # Generate report
        generator = ReportGenerator()
        report_path = generator.generate_html_report()
        
        print(f"📄 Report saved to: {report_path}")
        print("🌐 Open the HTML file in your browser to view the report")
        
    except Exception as e:
        print(f"❌ Error generating report: {e}")
        return False
    
    return True


if __name__ == "__main__":
    main()