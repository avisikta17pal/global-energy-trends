from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.utils import SCREENSHOTS_DIR, load_df
from src.visualization import choropleth_co2_per_capita, global_trends, country_time_series


def _safe_write_image(fig, out_path: Path) -> None:
    try:
        fig.write_image(str(out_path))
    except Exception:
        pass


def _safe_write_html(fig, out_path: Path) -> None:
    try:
        fig.write_html(str(out_path), include_plotlyjs="cdn", full_html=True)
    except Exception:
        pass


def main():
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    merged = load_df("merged.parquet")
    global_agg = load_df("global_aggregates.parquet")

    if merged is None or global_agg is None:
        raise SystemExit("Processed data not found. Run the Streamlit app once to generate data.")

    latest_year = int(merged["year"].max())

    # Global map
    fig_map = choropleth_co2_per_capita(merged, latest_year)
    _safe_write_image(fig_map, SCREENSHOTS_DIR / f"global_map_{latest_year}.png")
    _safe_write_html(fig_map, SCREENSHOTS_DIR / f"global_map_{latest_year}.html")

    # Global trend lines
    fig_trends = global_trends(global_agg)
    _safe_write_image(fig_trends, SCREENSHOTS_DIR / "global_trends.png")
    _safe_write_html(fig_trends, SCREENSHOTS_DIR / "global_trends.html")

    # Country example
    example_country = "United States" if "United States" in merged["country_standard"].unique() else merged["country_standard"].dropna().unique()[0]
    charts = country_time_series(merged, example_country)
    _safe_write_image(charts["co2_per_capita"], SCREENSHOTS_DIR / "country_comparison.png")
    _safe_write_html(charts["co2_per_capita"], SCREENSHOTS_DIR / "country_comparison.html")

    print("Visuals saved in:", SCREENSHOTS_DIR)


if __name__ == "__main__":
    main()