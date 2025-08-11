from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.utils import SCREENSHOTS_DIR, load_df
from src.visualization import choropleth_co2_per_capita, global_trends, country_time_series


def main():
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    merged = load_df("merged.parquet")
    global_agg = load_df("global_aggregates.parquet")

    if merged is None or global_agg is None:
        raise SystemExit("Processed data not found. Run the Streamlit app once to generate data.")

    # Global map for latest year
    latest_year = int(merged["year"].max())
    fig_map = choropleth_co2_per_capita(merged, latest_year)
    fig_map.write_image(str(SCREENSHOTS_DIR / f"global_map_{latest_year}.png"))

    # Global trend lines
    fig_trends = global_trends(global_agg)
    fig_trends.write_image(str(SCREENSHOTS_DIR / "global_trends.png"))

    # Country example
    example_country = "United States" if "United States" in merged["country_standard"].unique() else merged["country_standard"].dropna().unique()[0]
    charts = country_time_series(merged, example_country)
    charts["co2_per_capita"].write_image(str(SCREENSHOTS_DIR / "country_comparison.png"))

    print("Screenshots generated in:", SCREENSHOTS_DIR)


if __name__ == "__main__":
    main()