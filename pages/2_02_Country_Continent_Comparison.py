from __future__ import annotations

import streamlit as st
import pandas as pd

from src.utils import load_df
from src.visualization import country_time_series, continent_time_series

st.title("Country/Continent Comparison")

merged = load_df("merged.parquet")
if merged is None:
    st.error("Data not found. Please run the main app to generate processed data.")
    st.stop()

countries = sorted([c for c in merged.loc[~merged["is_aggregate"], "country_standard"].dropna().unique()])
continents = sorted([c for c in merged["continent"].dropna().unique()])

mode = st.radio("Compare by:", ["Country", "Continent"], horizontal=True)

if mode == "Country":
    country = st.selectbox("Select country", countries, index=countries.index("United States") if "United States" in countries else 0)
    charts = country_time_series(merged, country)
    st.caption("CO₂ per capita in tonnes/person; Renewable share as % of primary energy; GDP YoY as %.")
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(charts["co2_per_capita"], use_container_width=True)
        st.plotly_chart(charts["gdp_yoy"], use_container_width=True)
    with col2:
        st.plotly_chart(charts["renewables_share_energy"], use_container_width=True)
else:
    continent = st.selectbox("Select continent", continents, index=continents.index("Europe") if "Europe" in continents else 0)
    charts = continent_time_series(merged, continent)
    st.caption("Continent aggregates: CO₂ per capita derived from summed CO₂ and population; renewable share population-weighted; GDP YoY from summed GDP.")
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(charts["co2_per_capita"], use_container_width=True)
        st.plotly_chart(charts["gdp_yoy"], use_container_width=True)
    with col2:
        st.plotly_chart(charts["renewables_share_energy"], use_container_width=True)