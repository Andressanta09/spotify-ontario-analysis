# Spotify Ontario Music Analysis

Este proyecto analiza las tendencias musicales en playlists de Spotify relacionadas con Ontario, incluyendo análisis de características de audio, popularidad y patrones temporales.

## Estructura del Proyecto

```
spotify-ontario-analysis/
│
├── data/
│   ├── raw/               # Datos crudos extraídos (JSON, CSV)
│   ├── processed/         # Datos limpios (Parquet, CSV)
│   └── samples/           # Muestras pequeñas para pruebas
│
├── notebooks/
│   ├── 01_collect.ipynb   # Extracción de datos
│   ├── 02_clean.ipynb     # Limpieza y preprocesado
│   └── 03_analysis.ipynb  # Análisis exploratorio y modelado
│
├── dashboard/
│   ├── app.py             # Código del dashboard (Streamlit)
│   └── assets/            # Logos, íconos o imágenes
│
└── reports/               # Plantillas de informes
```

## Requisitos

- Python 3.8+
- Bibliotecas Python listadas en `requirements.txt`
- Credenciales de API de Spotify

## Configuración

1. Clonar el repositorio
2. Crear un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```
3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Copiar `.env.example` a `.env` y configurar las credenciales de Spotify

## Uso

1. Extracción de Datos:
   - Ejecutar `notebooks/01_collect.ipynb` para recolectar datos de Spotify
   
2. Procesamiento:
   - Ejecutar `notebooks/02_clean.ipynb` para limpiar y preprocesar los datos
   
3. Análisis:
   - Ejecutar `notebooks/03_analysis.ipynb` para el análisis exploratorio
   
4. Dashboard:
   ```bash
   cd dashboard
   streamlit run app.py
   ```

## Estructura de Datos

### Raw Data
- `playlists_*.csv`: Información básica de playlists
- `tracks_*.csv`: Información de canciones
- `audio_features_*.csv`: Características de audio

### Processed Data
- Archivos Parquet con datos limpios y procesados
- Datos de muestra para pruebas rápidas

## Dashboard

El dashboard incluye:
- Vista general de métricas clave
- Análisis temporal de características musicales
- Distribuciones de features de audio
- Rankings de popularidad

## Contribuir

1. Fork del repositorio
2. Crear una rama para features: `git checkout -b feature/nombre`
3. Commit de cambios: `git commit -am 'Añadir feature'`
4. Push a la rama: `git push origin feature/nombre`
5. Crear Pull Request