"""Visualization helpers using Plotly and seaborn/matplotlib where needed."""
from __future__ import annotations

from typing import Optional

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def choropleth_co2_per_capita(df: pd.DataFrame, year: int) -> px.choropleth:
    d = df[(df["year"] == year) & (~df["is_aggregate"])].copy()
    # Drop rows without ISO-3 codes or values
    d = d.dropna(subset=["iso_code", "co2_per_capita"]).copy()
    if d.empty:
        fig = go.Figure()
        fig.update_layout(title_text=f"No map data available for year {year}")
        return fig
    fig = px.choropleth(
        d,
        locations="iso_code",
        color="co2_per_capita",
        hover_name="country_standard",
        color_continuous_scale="YlOrRd",
        labels={"co2_per_capita": "CO₂ per capita (t/person)"},
        title=f"CO₂ per capita by country — {year}",
    )
    fig.update_geos(showcountries=True, showcoastlines=False, showland=True, fitbounds="locations")
    fig.update_layout(margin=dict(l=0, r=0, t=50, b=0))
    return fig


def global_trends(global_df: pd.DataFrame):
    d = global_df.sort_values("year")
    fig = px.line(
        d.melt(id_vars=["year"], value_vars=["co2_per_capita_global", "renewables_share_global"], var_name="metric", value_name="value"),
        x="year", y="value", color="metric",
        labels={"value": "Value", "metric": "Metric"},
        title="Global CO₂ per capita and Renewable Share over time",
    )
    return fig


def country_time_series(df: pd.DataFrame, country: str) -> dict[str, object]:
    d = df[(df["country_standard"] == country)].sort_values("year")
    charts = {}

    charts["co2_per_capita"] = px.line(
        d, x="year", y="co2_per_capita", title=f"CO₂ per capita — {country}", labels={"co2_per_capita": "t/person"}
    )
    charts["renewables_share_energy"] = px.line(
        d, x="year", y="renewables_share_energy", title=f"Renewables Share — {country}", labels={"renewables_share_energy": "% of energy"}
    )
    charts["gdp_yoy"] = px.line(
        d, x="year", y="gdp_yoy", title=f"GDP YoY Growth — {country}", labels={"gdp_yoy": "%"}
    )
    return charts


def continent_time_series(df: pd.DataFrame, continent: str) -> dict[str, object]:
    d = df[(df["continent"] == continent) & (~df["is_aggregate"])].copy()
    # Aggregate by year with population weighting and compute YoY from aggregated GDP
    d_year = d.groupby("year").agg(
        total_co2=("co2", "sum"),
        total_population=("population", "sum"),
        weighted_renewables=("renewables_share_energy", lambda s: (s * d.loc[s.index, "population"]).sum(min_count=1)),
        total_gdp=("gdp", "sum"),
    ).reset_index()
    d_year["co2_per_capita"] = (d_year["total_co2"] * 1e6) / d_year["total_population"]
    d_year["renewables_share_energy"] = d_year["weighted_renewables"] / d_year["total_population"]
    d_year = d_year.sort_values("year")
    d_year["gdp_yoy"] = d_year["total_gdp"].pct_change() * 100.0

    charts = {}
    charts["co2_per_capita"] = px.line(
        d_year, x="year", y="co2_per_capita", title=f"CO₂ per capita — {continent}", labels={"co2_per_capita": "t/person"}
    )
    charts["renewables_share_energy"] = px.line(
        d_year, x="year", y="renewables_share_energy", title=f"Renewables Share — {continent}", labels={"renewables_share_energy": "% of energy"}
    )
    charts["gdp_yoy"] = px.line(
        d_year, x="year", y="gdp_yoy", title=f"GDP YoY Growth — {continent}", labels={"gdp_yoy": "%"}
    )
    return charts