# 🌍 Global CO₂ Emissions and Renewable Energy Trends: 1990–2023

A complete, end-to-end data storytelling and visualization project that explores the relationship between CO₂ emissions, renewable energy adoption, and GDP growth across countries from 1990 to 2023.

This project automatically downloads data from open sources, cleans and combines them, performs exploratory data analysis (EDA), and provides an interactive Streamlit dashboard to tell a compelling data story.

## Project Goals
- Analyze long-run trends in CO₂ emissions and renewable energy adoption.
- Explore the relationship between GDP growth, CO₂ emissions, and renewable adoption.
- Provide interactive visualizations at global, continent, and country levels.
- Summarize key insights and highlight notable events (e.g., Paris Agreement 2015).

## Features
- Automated data acquisition from Our World in Data (OWID), or upload your own processed CSVs via the sidebar
- Clean, merge, and enrich datasets with derived metrics:
  - CO₂ per capita
  - Renewable energy YoY growth rate
  - GDP YoY growth rate
  - Continent classification
- EDA with summary stats, correlations, and rankings
- Streamlit dashboard with three pages:
  - Global Overview: world map of CO₂ per capita by year using Plotly choropleth; global trends of CO₂ per capita and renewable share.
  - Country/Continent Comparison: interactive time-series for emissions intensity, renewable adoption, and GDP growth.
  - Insights & Story: narrative with notable events and contextual interpretation.
- Programmatically generated example screenshots
- Modular, PEP8-compliant Python codebase

## Dataset Sources
- CO₂ data: Our World in Data — `owid-co2-data.csv`  
  Raw CSV: [`https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv`](https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv)
- Energy data: Our World in Data — `owid-energy-data.csv`  
  Raw CSV: [`https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv`](https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv)

Columns used:
- From `owid-co2-data.csv`: `country`, `iso_code`, `year`, `co2` (million tonnes), `co2_per_capita` (t/person), `gdp` (US$), `population`.
- From `owid-energy-data.csv`: `country`, `iso_code`, `year`, `renewables_share_energy` (% of primary energy).

## Project Structure
```
global_co2_renewables/
├─ app.py
├─ pages/
│  ├─ 1_01_Global_Overview.py
│  ├─ 2_02_Country_Continent_Comparison.py
│  └─ 3_03_Insights_and_Story.py
├─ src/
│  ├─ __init__.py
│  ├─ utils.py
│  ├─ data_acquisition.py
│  ├─ data_processing.py
│  ├─ eda.py
│  └─ visualization.py
├─ scripts/
│  └─ generate_screenshots.py
├─ data/
│  ├─ raw/
│  └─ processed/
├─ assets/
│  └─ screenshots/
├─ .streamlit/
│  └─ config.toml
├─ requirements.txt
└─ README.md
```

## Quickstart

1) Create and activate a virtual environment (recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

2) Install dependencies

```bash
pip install -r requirements.txt
```

3) Run the Streamlit app

```bash
streamlit run app.py
```

Note on Python version: use Python 3.11 for fastest, wheel-based installs on Streamlit Cloud.

The app will:
- Automatically download raw data into `data/raw/` (unless you upload your own processed CSVs)
- Process and cache a merged dataset into `data/processed/` (Parquet if available, else CSV)
- Launch the dashboard at a local URL

4) Generate example screenshots (optional)

```bash
python scripts/generate_screenshots.py
```

Screenshots will be saved to `assets/screenshots/`.

## EDA (Built-in & Command-line)
- In-app: use the pages to explore global trends and make country/continent comparisons. Top/bottom countries and correlation analysis are accessible via code helpers.
- Command-line quicklook:
```python
import pandas as pd
from src.utils import load_df
from src.eda import summary_statistics, correlations, top_bottom_by_co2_per_capita

merged = load_df("merged.parquet")
print(summary_statistics(merged))
print(correlations(merged))
print(top_bottom_by_co2_per_capita(merged, 2023))
```

## Run data pipeline only (optional)
If you prefer to pre-generate processed data without launching the app:
```python
from src.data_acquisition import load_raw_datasets
from src.data_processing import build_processed_dataset
co2, energy = load_raw_datasets()
_ = build_processed_dataset(co2, energy)
```
This creates `data/processed/merged.parquet` and `data/processed/global_aggregates.parquet`.

## Usage Notes
- Year range is constrained to 1990–2023 where data availability is robust.
- Aggregates like world and regions (e.g., `OWID_WRL`) are excluded from maps but used for global trend calculations.
- Global trends are computed using population-weighted averages for renewable shares and sums for CO₂, with CO₂ per capita derived from total CO₂ divided by total population.

## Deployment

### Streamlit Community Cloud
- Push this repository to GitHub
- On Streamlit Cloud, create a new app pointing to `app.py`
- Set Python version to 3.11 (recommended) and provide `requirements.txt`
- No system packages are required. All maps use Plotly choropleth.
- No secrets are required

### Hugging Face Spaces
- Create a new Space (SDK: Streamlit)
- Upload all project files
- Ensure `requirements.txt` is present
- Set the `app.py` as the entrypoint

## Screenshots
Programmatically generated examples (you can regenerate via the script):

![Global map (example)](assets/screenshots/global_map_2023.png)

![Global trends (example)](assets/screenshots/global_trends.png)

![Country comparison (example)](assets/screenshots/country_comparison.png)

## Troubleshooting
- If maps render blank, ensure `iso_code` is present for countries (auto-handled) and your network allows the OWID downloads.
- If static image export fails in `generate_screenshots.py`, install Kaleido:
  - `pip install -U kaleido`

## Key Insights (Preview)
- Post-2000, rapid industrialization in parts of Asia increased global CO₂, while per-capita trends diverged across regions.
- The Paris Agreement (2015) coincides with accelerating renewable adoption in many countries, though the effect sizes vary.
- CO₂ intensity per capita shows notable declines in Europe, with mixed trends elsewhere.
- GDP growth correlates positively with renewable adoption in many contexts, though causality is nuanced and country-specific.

## Contributing
- Follow PEP8 and keep functions small and well-named.
- Use `src/` modules; avoid putting logic directly in page files.
- Add docstrings to public functions and keep comments focused on "why".
- For new visuals, add helpers to `src/visualization.py` and call from pages.

## License
MIT License. See `LICENSE` if included, or adapt as needed for your use.