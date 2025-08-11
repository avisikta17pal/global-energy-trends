"""Exploratory Data Analysis utilities."""
from __future__ import annotations

import pandas as pd


def summary_statistics(df: pd.DataFrame) -> pd.DataFrame:
    cols = [c for c in ["co2", "co2_per_capita", "renewables_share_energy", "gdp", "population", "renewables_share_yoy", "gdp_yoy"] if c in df.columns]
    return df[cols].describe(percentiles=[0.1, 0.25, 0.5, 0.75, 0.9]).T


def correlations(df: pd.DataFrame) -> pd.DataFrame:
    cols = [c for c in ["co2", "co2_per_capita", "renewables_share_energy", "gdp", "population", "renewables_share_yoy", "gdp_yoy"] if c in df.columns]
    return df[cols].corr(method="pearson")


def top_bottom_by_co2_per_capita(df: pd.DataFrame, year: int, top_n: int = 10) -> tuple[pd.DataFrame, pd.DataFrame]:
    d = df[(df["year"] == year) & (~df["is_aggregate"])].copy()
    d = d.dropna(subset=["co2_per_capita"]).copy()
    top = d.nlargest(top_n, "co2_per_capita")[
        ["country_standard", "co2_per_capita", "co2", "population", "renewables_share_energy"]
    ]
    bottom = d.nsmallest(top_n, "co2_per_capita")[
        ["country_standard", "co2_per_capita", "co2", "population", "renewables_share_energy"]
    ]
    return top, bottom


def renewable_trend(df: pd.DataFrame, country_or_continent: str, value: str = "country") -> pd.DataFrame:
    if value == "continent":
        d = df[~df["is_aggregate"]].groupby(["continent", "year"]).apply(
            lambda g: (g["renewables_share_energy"] * g["population"]).sum(min_count=1) / g["population"].sum(min_count=1)
        ).reset_index(name="renewables_share_energy")
        return d
    else:
        return df[(df["country_standard"] == country_or_continent)].sort_values("year")["year"].to_frame().assign(
            renewables_share_energy=df[(df["country_standard"] == country_or_continent)].sort_values("year")["renewables_share_energy"].values
        )


def gdp_vs_renewables_corr(df: pd.DataFrame) -> pd.DataFrame:
    d = df[["country_standard", "year", "gdp_yoy", "renewables_share_yoy"]].dropna()
    # Compute per-country correlation between GDP YoY and Renewables YoY
    corr = (
        d.groupby("country_standard")[ ["gdp_yoy", "renewables_share_yoy"] ]
        .corr()
        .reset_index()
    )
    # Extract correlation of gdp_yoy with renewables_share_yoy
    corr = corr[(corr["level_1"] == "renewables_share_yoy") & (corr["gdp_yoy"].notna())][["country_standard", "gdp_yoy"]]
    corr = corr.rename(columns={"gdp_yoy": "corr"}).sort_values("corr", ascending=False)
    return corr