# 📊 Analysis Reports

This directory contains automatically generated analysis reports from the Spotify Ontario music data.

## 📄 Report Types

### 🌐 HTML Reports
Interactive HTML reports with visualizations and comprehensive analysis:
- **File Pattern:** `ontario_music_analysis_report_YYYYMMDD_HHMMSS.html`
- **Content:** Charts, statistics, trends, and insights
- **Format:** Self-contained HTML with embedded Plotly charts

## 🚀 Generating Reports

### Automatic Generation
```bash
# From project root directory
python generate_report.py
```

### From Notebooks
Reports can also be generated from the analysis notebook:
```python
# In 03_analysis.ipynb
from generate_report import ReportGenerator

generator = ReportGenerator()
report_path = generator.generate_html_report()
```

## 📋 Report Contents

Each report includes:

### 📊 Summary Statistics
- Total tracks analyzed
- Number of playlists
- Unique artists and albums
- Date range coverage

### 📈 Visualizations
- **Popularity Distribution:** Track popularity scores
- **Audio Features Profile:** Radar chart of average features
- **Top Artists:** Most represented artists
- **Temporal Trends:** How music characteristics evolve over time
- **Feature Correlations:** Relationships between audio features

### 🎯 Key Insights
- Musical trends in Ontario
- Popular characteristics
- Artist diversity
- Genre representations

## 🔍 Report Features

### Interactive Elements
- **Hover Information:** Detailed data on chart hover
- **Zoom/Pan:** Navigate large datasets
- **Responsive Design:** Works on desktop and mobile

### Data Quality Indicators
- Missing data notifications
- Sample size information
- Data source timestamps

## 📁 File Organization

Reports are automatically timestamped and organized by:
- **Date Generated:** YYYY-MM-DD format
- **Time Generated:** HH-MM-SS format
- **Consistent Naming:** Easy to identify latest reports

## 🎨 Customization

### Styling
Reports use Spotify-inspired color scheme:
- **Primary Green:** #1DB954 (Spotify brand color)
- **Clean Layout:** Professional presentation
- **Responsive Design:** Mobile-friendly

### Content Sections
Each report automatically adapts to available data:
- Shows relevant visualizations
- Hides sections with no data
- Provides helpful explanations

## 📊 Sample Analysis Areas

### Musical Characteristics
- **Danceability:** How suitable for dancing
- **Energy:** Intensity and power
- **Valence:** Musical positivity
- **Acousticness:** Acoustic vs electronic
- **Tempo:** Beats per minute

### Temporal Analysis
- Trends over decades
- Seasonal patterns
- Era-specific characteristics

### Artist & Content Analysis
- Most popular artists
- Genre distribution
- Album representation
- Release patterns

## 🔄 Automation

### Scheduled Generation
You can automate report generation:

```python
# Daily reports
import schedule
import time

def generate_daily_report():
    generator = ReportGenerator()
    generator.generate_html_report()

schedule.every().day.at("09:00").do(generate_daily_report)

while True:
    schedule.run_pending()
    time.sleep(1)
```

### Integration Options
- **Dashboard Updates:** Sync with Streamlit dashboard
- **Email Reports:** Send automatically via email
- **Cloud Storage:** Upload to cloud platforms

## 🎯 Best Practices

### Data Quality
- Ensure clean data before generating reports
- Run data validation checks
- Document any data limitations

### Report Management
- Keep latest 10 reports for comparison
- Archive older reports
- Regular cleanup of old files

### Sharing
- Reports are self-contained HTML files
- No external dependencies for viewing
- Easy to share via email or cloud storage

---

📈 **Latest Report:** Check timestamps to find the most recent analysis
🔄 **Updates:** Reports reflect the latest processed data
📧 **Questions?** See main project README for support information