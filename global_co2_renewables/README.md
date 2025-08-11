# 🌍 Global CO₂ Emissions and Renewable Energy Trends (1990–2023)

An end‑to‑end data storytelling and visualization project exploring how CO₂ emissions, renewable energy adoption, and GDP growth have evolved across countries since 1990. The project provides a streamlined Streamlit dashboard, repeatable processing utilities, and minimal dependencies for smooth local runs and cloud deployment.

## Live app
- Open the Streamlit app: [Global Energy Trends](https://global-energy-trends-iccj6f96jeveueo7hkmpmf.streamlit.app/)

## What the app provides
- Turns your country‑year dataset into an interactive story about climate and energy
- Validates your uploaded data and computes population‑weighted global aggregates
- Calculates and visualizes key metrics:
  - CO₂ per capita (tonnes/person)
  - Renewable energy share and its YoY growth (%)
  - GDP YoY growth (%)
- Visual layers designed to answer different questions:
  - Global Overview: world map (choropleth) + global time‑series
  - Country/Continent Comparison: side‑by‑side time‑series for fair comparisons
  - Insights & Story: headline metrics and notable milestones (e.g., Paris Agreement 2015)
- Built‑in EDA helpers:
  - Top/Bottom countries by CO₂ per capita (for a selected year)
  - Correlation matrix across core metrics
- Output options:
  - Optional export of figures as HTML (always) and PNG (when static export is available)
- Offline‑first and deploy‑ready:
  - Works without internet data fetching
  - Minimal dependencies; Streamlit Cloud‑friendly (Python 3.11)

## Download my dataset
I provide a ready‑to‑use CSV so you can try the dashboard right away:
- [Download merged.csv](assets/data/merged.csv)

After downloading, open the app and use the sidebar to upload the file. The app will compute `global_aggregates.csv` automatically if you don’t upload it.

## Expected CSV columns
Your `merged.csv` should include these columns:
`country_standard, iso_code, year, co2, co2_per_capita, gdp, population, renewables_share_energy, renewables_share_yoy, gdp_yoy, continent, is_aggregate`

Tip: In the app sidebar, I also include a quick template download with just the headers if you’re preparing the file yourself.

## Features
- Upload‑first workflow (no automatic internet fetches)
- Clean, CSV‑friendly processing and caching (Parquet if available, else CSV)
- Plotly‑based maps (no geopandas/pyproj required)
- Modular code: separate processing, EDA, and visualization
- Minimal requirements for faster and more reliable deployments

## Project structure
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
2) Install dependencies
```bash
pip install -r requirements.txt
```
3) Start the app
```bash
streamlit run app.py
```
4) Upload `merged.csv` via the sidebar. Alternatively, place it at `data/processed/merged.csv` before launching.

## Data handling
- The app loads your uploaded CSV and caches processed outputs locally.
- If you do not upload `global_aggregates.csv`, the app computes it from your merged file.
- All mapping uses Plotly choropleth with ISO‑3 codes from your data.

## Deployment
- Streamlit Community Cloud: point to `app.py`, include `requirements.txt`, and use Python 3.11 (via `runtime.txt`).
- After deployment, upload `merged.csv` from the sidebar (or include it under `data/processed/` in the repo if you want it loaded automatically).

## Contributing
- Suggestions and improvements are welcome—feel free to open an issue or PR.
- If you publish a dataset with the repo, add a short note at `data/processed/DATASET_README.md` with source and license.

## License
MIT. See `LICENSE`.