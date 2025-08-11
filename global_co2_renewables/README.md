# 🌍 Global CO₂ Emissions and Renewable Energy Trends: 1990–2023

A complete, end-to-end data storytelling and visualization project that explores the relationship between CO₂ emissions, renewable energy adoption, and GDP growth across countries from 1990 to 2023.

This project loads your provided processed datasets, performs exploratory data analysis (EDA), and provides an interactive Streamlit dashboard to tell a compelling data story. You can generate processed data offline (e.g., with Kaggle sources) and upload it to the app.

## Project Goals
- Analyze long-run trends in CO₂ emissions and renewable energy adoption.
- Explore the relationship between GDP growth, CO₂ emissions, and renewable adoption.
- Provide interactive visualizations at global, continent, and country levels.
- Summarize key insights and highlight notable events (e.g., Paris Agreement 2015).

## Features
- Upload your own processed CSVs via the sidebar (offline-friendly; no internet fetching)
- Clean, merge, and enrich datasets with derived metrics (if you run the processing offline):
  - CO₂ per capita
  - Renewable energy YoY growth rate
  - GDP YoY growth rate
  - Continent classification
- EDA with summary stats, correlations, and rankings
- Streamlit dashboard with three pages:
  - Global Overview: world map of CO₂ per capita by year using Plotly choropleth; global trends of CO₂ per capita and renewable share.
  - Country/Continent Comparison: interactive time-series for emissions intensity, renewable adoption, and GDP growth.
  - Insights & Story: narrative with notable events and contextual interpretation.
- Programmatically generated example screenshots/HTML visuals
- Modular, PEP8-compliant Python codebase

## Expected CSV Inputs
Place or upload these files (headers required). If you plan to publish the repo with your data, include a dataset README at `data/processed/DATASET_README.md` describing source and license.
- `data/processed/merged.csv` (or upload via sidebar)
  - columns: `country_standard`, `iso_code`, `year`, `co2`, `co2_per_capita`, `gdp`, `population`, `renewables_share_energy`, `renewables_share_yoy`, `gdp_yoy`, `continent`, `is_aggregate`
- `data/processed/global_aggregates.csv` (optional; if missing, app computes from merged)
  - columns: `year`, `co2_global`, `population_global`, `renewables_share_global`, `co2_per_capita_global`

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
├─ runtime.txt
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

3) Prepare data (offline)
- Generate your processed CSVs externally (e.g., from Kaggle or OWID scripts)
- Either place them in `data/processed/merged.csv` and optionally `global_aggregates.csv`, or upload via the app sidebar

4) Run the Streamlit app

```bash
streamlit run app.py
```

The app will:
- Load your uploaded/placed data from `data/processed/`
- Compute `global_aggregates.csv` if missing
- Launch the dashboard at a local URL

5) Generate example visuals (optional)

```bash
python scripts/generate_screenshots.py
```

Screenshots and HTML visuals will be saved to `assets/screenshots/`.

## EDA (Built-in & Command-line)
- In-app: use the pages to explore global trends and make country/continent comparisons. Top/bottom countries and correlation analysis are accessible via code helpers.
- Command-line quicklook (requires merged CSV present):
```python
import pandas as pd
from src.utils import load_df
from src.eda import summary_statistics, correlations, top_bottom_by_co2_per_capita

merged = load_df("merged.parquet")  # or reads CSV fallback
print(summary_statistics(merged))
print(correlations(merged))
print(top_bottom_by_co2_per_capita(merged, 2023))
```

## Deployment

### Streamlit Community Cloud
- Push this repository to GitHub
- On Streamlit Cloud, create a new app pointing to `app.py`
- Set Python version to 3.11 (recommended) and provide `requirements.txt`
- No system packages are required. All maps use Plotly choropleth.
- Upload your processed CSVs via the app after deploy (or include them in the repo under `data/processed/`)

### Hugging Face Spaces
- Create a new Space (SDK: Streamlit)
- Upload all project files
- Ensure `requirements.txt` is present
- Set the `app.py` as the entrypoint
- Upload your processed CSVs via the app after deploy (or include them in the repo under `data/processed/`)

## Troubleshooting
- If maps render blank, ensure `iso_code` is present for countries and your uploaded files match the column expectations.
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