"""Data processing: clean, merge, and derive metrics for analysis (1990–2023)."""
from __future__ import annotations

from typing import Tuple

import numpy as np
import pandas as pd

from .utils import Constants, add_continent, ensure_directories, save_df, standardize_countries


def _filter_years(df: pd.DataFrame, year_col: str = "year", c: Constants = Constants()) -> pd.DataFrame:
    return df[(df[year_col] >= c.start_year) & (df[year_col] <= c.end_year)].copy()


def clean_co2_data(co2: pd.DataFrame) -> pd.DataFrame:
    use_cols = [
        "country",
        "iso_code",
        "year",
        "co2",  # total CO2 emissions (million tonnes)
        "co2_per_capita",  # tonnes per person
        "gdp",
        "population",
    ]
    co2 = co2[use_cols].copy()
    co2 = co2.dropna(subset=["year"]).copy()
    co2["year"] = co2["year"].astype(int)
    co2 = standardize_countries(co2, country_col="country")
    return _filter_years(co2)


def clean_energy_data(energy: pd.DataFrame) -> pd.DataFrame:
    use_cols = [
        "country",
        "iso_code",
        "year",
        "renewables_share_energy",  # % of primary energy
    ]
    energy = energy[use_cols].copy()
    energy = energy.dropna(subset=["year"]).copy()
    energy["year"] = energy["year"].astype(int)
    energy = standardize_countries(energy, country_col="country")
    return _filter_years(energy)


def merge_datasets(co2: pd.DataFrame, energy: pd.DataFrame) -> pd.DataFrame:
    df = pd.merge(
        co2,
        energy[["iso_code", "country_standard", "year", "renewables_share_energy"]],
        on=["iso_code", "year"],
        how="outer",
        suffixes=("_co2", "_energy"),
    )

    if "country_standard_co2" in df.columns and "country_standard_energy" in df.columns:
        df["country_standard"] = df["country_standard_co2"].fillna(df["country_standard_energy"])
        df.drop(columns=["country_standard_co2", "country_standard_energy"], inplace=True)
    elif "country_standard_co2" in df.columns:
        df.rename(columns={"country_standard_co2": "country_standard"}, inplace=True)
    elif "country_standard_energy" in df.columns:
        df.rename(columns={"country_standard_energy": "country_standard"}, inplace=True)

    missing_iso = df[df["iso_code"].isna()][["country_standard", "year", "renewables_share_energy"]]
    if not missing_iso.empty:
        fallback = pd.merge(
            df.drop(columns=["renewables_share_energy"]),
            missing_iso,
            on=["country_standard", "year"],
            how="left",
        )
        df = fallback

    df = add_continent(df, iso_col="iso_code")

    for col in ["co2", "co2_per_capita", "gdp", "population", "renewables_share_energy"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Compute CO₂ per capita if missing and population available. Result is tonnes/person.
    df["co2_per_capita"] = df["co2_per_capita"].fillna(
        np.where((df["co2"].notna()) & (df["population"].notna()) & (df["population"] > 0),
                 (df["co2"] * 1e6) / df["population"],
                 np.nan)
    )

    df = df.sort_values(["country_standard", "year"]).copy()
    df["renewables_share_yoy"] = df.groupby("country_standard")["renewables_share_energy"].pct_change() * 100.0
    df["gdp_yoy"] = df.groupby("country_standard")["gdp"].pct_change() * 100.0

    df["is_aggregate"] = df["iso_code"].astype(str).str.startswith("OWID_")

    return df


def compute_global_aggregates(df: pd.DataFrame) -> pd.DataFrame:
    grp = df[~df["is_aggregate"]].groupby("year")
    total_co2 = grp["co2"].sum(min_count=1)
    total_pop = grp["population"].sum(min_count=1)
    pop_weighted_renewables = grp.apply(
        lambda g: (g["renewables_share_energy"] * g["population"]).sum(min_count=1) / g["population"].sum(min_count=1)
    )

    result = pd.DataFrame({
        "year": total_co2.index,
        "co2_global": total_co2.values,
        "population_global": total_pop.values,
        "renewables_share_global": pop_weighted_renewables.values,
    })
    result["co2_per_capita_global"] = (result["co2_global"] * 1e6) / result["population_global"]
    return result


def build_processed_dataset(co2: pd.DataFrame, energy: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    ensure_directories()
    co2_clean = clean_co2_data(co2)
    energy_clean = clean_energy_data(energy)
    merged = merge_datasets(co2_clean, energy_clean)
    global_agg = compute_global_aggregates(merged)
    save_df(merged, "merged.parquet")
    save_df(global_agg, "global_aggregates.parquet")
    return merged, global_agg