# Spotify Ontario Music Analysis

This project analyzes music trends in Spotify playlists related to Ontario, including analysis of audio features, popularity, and temporal patterns.

## Project Structure

```
spotify-ontario-analysis/
│
├── data/
│   ├── raw/               # Raw extracted data (JSON, CSV)
│   ├── processed/         # Clean data (Parquet, CSV)
│   └── samples/           # Small samples for testing
│
├── notebooks/
│   ├── 01_collect.ipynb   # Data extraction
│   ├── 02_clean.ipynb     # Cleaning and preprocessing
│   └── 03_analysis.ipynb  # Exploratory analysis and modeling
│
├── dashboard/
│   ├── app.py             # Dashboard code (Streamlit)
│   └── assets/            # Logos, icons, or images
│
└── reports/               # Report templates
```

## Requirements

- Python 3.8+
- Python libraries listed in `requirements.txt`
- Spotify API credentials

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and configure Spotify credentials

## Usage

1. Data Extraction:
   - Run `notebooks/01_collect.ipynb` to collect data from Spotify
   
2. Processing:
   - Run `notebooks/02_clean.ipynb` to clean and preprocess the data
   
3. Analysis:
   - Run `notebooks/03_analysis.ipynb` for exploratory analysis
   
4. Dashboard:
   ```bash
   cd dashboard
   streamlit run app.py
   ```

## Data Structure

### Raw Data
- `playlists_*.csv`: Basic playlist information
- `tracks_*.csv`: Track information
- `audio_features_*.csv`: Audio features

### Processed Data
- Parquet files with clean and processed data
- Sample data for quick testing

## Dashboard

The dashboard includes:
- Overview of key metrics
- Temporal analysis of musical features
- Audio feature distributions
- Popularity rankings

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to the branch: `git push origin feature/name`
5. Create Pull Request