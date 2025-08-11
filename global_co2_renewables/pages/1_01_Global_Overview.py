from __future__ import annotations

import streamlit as st
import pandas as pd

from src.utils import load_df, Constants
from src.visualization import choropleth_co2_per_capita, global_trends
from src.eda import top_bottom_by_co2_per_capita, correlations

st.title("Global Overview")

merged = load_df("merged.parquet")
global_agg = load_df("global_aggregates.parquet")

if merged is None or global_agg is None:
    st.error("Data not found. Please run the main app to generate processed data.")
    st.stop()

c = Constants()
year = st.slider("Select year", min_value=c.start_year, max_value=c.end_year, value=c.end_year, step=1)

st.subheader("World map: CO₂ per capita")
st.caption("Tonnes of CO₂ per person. Aggregates and regions are excluded.")
fig_map = choropleth_co2_per_capita(merged, year)
st.plotly_chart(fig_map, use_container_width=True)

st.subheader("Global CO₂ per capita vs Renewable Share")
st.caption("Population-weighted renewable share; CO₂ per capita computed from total CO₂ and population.")
fig_trend = global_trends(global_agg)
st.plotly_chart(fig_trend, use_container_width=True)

with st.expander("Top/Bottom 10 countries by CO₂ per capita"):
    top, bottom = top_bottom_by_co2_per_capita(merged, year, top_n=10)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Top 10**")
        st.dataframe(top, use_container_width=True)
    with col2:
        st.markdown("**Bottom 10**")
        st.dataframe(bottom, use_container_width=True)

with st.expander("Correlation matrix (selected metrics)"):
    corr = correlations(merged)
    st.dataframe(corr, use_container_width=True)