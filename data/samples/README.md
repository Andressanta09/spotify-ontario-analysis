# Spotify Ontario Analysis - Sample Data

This directory contains sample data files to help understand the data structure and test the analysis pipeline.

## 📁 Sample Files

### 🎵 `sample_tracks.csv`
Small sample of track data with the following structure:
- **Track Information:** name, artist, album, duration
- **Spotify Metadata:** track_id, popularity, release_date
- **Audio Features:** danceability, energy, valence, tempo, etc.
- **Playlist Context:** playlist_id, playlist_name

### 🎼 `sample_playlists.csv`
Sample playlist metadata including:
- **Playlist Info:** id, name, description, owner
- **Statistics:** followers, tracks_total, public status
- **Timestamps:** created_at, updated_at

### 📊 `data_dictionary.json`
Complete data dictionary explaining all fields and their meanings.

## 🎯 Usage

These sample files are useful for:

1. **Testing:** Run analysis on small datasets
2. **Understanding:** Learn the data structure
3. **Development:** Test new features safely
4. **Documentation:** Show expected data formats

## 🚀 Getting Started

To use sample data:

```python
import pandas as pd

# Load sample tracks
tracks_df = pd.read_csv('data/samples/sample_tracks.csv')

# Load sample playlists  
playlists_df = pd.read_csv('data/samples/sample_playlists.csv')

# View structure
print(tracks_df.info())
print(playlists_df.head())
```

## 📈 Next Steps

1. Explore the sample data
2. Run notebooks with sample data for testing
3. Collect your own data using the collection notebook
4. Apply the same analysis to your larger dataset

---

💡 **Tip:** Always test with sample data before processing large datasets!