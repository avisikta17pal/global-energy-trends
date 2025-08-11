# 🌍 Global CO₂ Emissions and Renewable Energy Trends (1990–2023)

I built this project to tell a clear, data‑driven story about how CO₂ emissions, renewable energy adoption, and GDP growth have evolved across countries since 1990. It’s a Streamlit app with interactive maps and time‑series charts, backed by a simple, robust data pipeline.

## What this app does
- Lets you upload a prepared dataset (CSV), then explores:
  - CO₂ per capita trends (global and by country/continent)
  - Renewable energy share and its year‑over‑year change
  - GDP year‑over‑year growth
- Shows a global choropleth map, interactive time‑series charts, and a short narrative with key milestones (e.g., Paris Agreement 2015).

## Download my dataset
I provide a ready‑to‑use CSV so you can try the dashboard right away:
- [Download merged.csv](assets/data/merged.csv)

After downloading, open the app and use the sidebar to upload the file. The app will compute `global_aggregates.csv` automatically if you don’t upload it.

## Expected CSV columns
Your `merged.csv` should include these columns:
`country_standard, iso_code, year, co2, co2_per_capita, gdp, population, renewables_share_energy, renewables_share_yoy, gdp_yoy, continent, is_aggregate`

Tip: In the app sidebar, I also include a quick template download with just the headers if you’re preparing the file yourself.

## Project structure (high level)
```
global_co2_renewables/
├─ app.py                  # Streamlit entrypoint
├─ pages/                  # Streamlit pages
├─ src/                    # Data processing, EDA, viz helpers
├─ scripts/                # Screenshot generator
├─ assets/
│  ├─ screenshots/         # Optional exported figures
│  └─ data/                # Place merged.csv here for README download
├─ data/
│  └─ processed/           # App reads finished CSVs from here (if preplaced)
├─ requirements.txt        # Minimal, Streamlit‑friendly deps
├─ runtime.txt             # Pin Python to 3.11 on Streamlit Cloud
└─ README.md
```

## Run locally
1) Create a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```
2) Install deps
```bash
pip install -r requirements.txt
```
3) Start the app
```bash
streamlit run app.py
```
4) Upload `merged.csv` via the sidebar and explore. If you prefer, you can also place it at `data/processed/merged.csv` before launching.

## Notes on data handling
- The app reads your uploaded CSV and caches processed data locally (Parquet if available, otherwise CSV).
- If you don’t provide `global_aggregates.csv`, the app computes it from your merged file.
- I removed heavy geo/system dependencies (geopandas/pyproj). Maps use Plotly choropleth with ISO‑3 codes from your file.

## Deployment
- Streamlit Community Cloud: point it to `app.py`, include `requirements.txt`, and use Python 3.11 (I include `runtime.txt`).
- After deploy, upload `merged.csv` from the sidebar (or include it under `data/processed/` in the repo if you want it loaded automatically).

## Why I built it this way
I wanted an analysis that is easy to run anywhere (local or Streamlit Cloud) and doesn’t break on system packages. That’s why I:
- Use Plotly choropleth instead of geopandas/pyproj
- Keep the pipeline simple and CSV‑friendly
- Provide a clean UI with three focused pages: Global Overview, Country/Continent Comparison, and Insights & Story

## Contributing
- I welcome suggestions and improvements. Please open an issue or PR.
- If you publish your own dataset with the repo, add a short note at `data/processed/DATASET_README.md` with source and license.

## License
MIT. See `LICENSE`.