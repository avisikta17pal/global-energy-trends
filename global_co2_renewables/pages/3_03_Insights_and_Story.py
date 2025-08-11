from __future__ import annotations

import streamlit as st
import pandas as pd

from src.utils import load_df, Constants

st.title("Insights & Story")

merged = load_df("merged.parquet")
global_agg = load_df("global_aggregates.parquet")

if merged is None or global_agg is None:
    st.error("Data not found. Please run the main app to generate processed data.")
    st.stop()

c = Constants()

st.markdown(
    f"""
### Narrative
- The period {c.start_year}–{c.end_year} shows divergent trajectories between total CO₂ emissions and CO₂ intensity per capita across regions.
- The Paris Agreement in {c.paris_agreement_year} marked a global commitment; following this, several countries accelerated renewable adoption.
- Economic growth (GDP YoY) and renewable growth often move together, but causality depends on energy policies, technology costs, and sectoral mix.

### Highlights
- Countries in Europe exhibit sustained increases in renewables share with flat-to-declining CO₂ per capita.
- Some emerging economies increased renewables while still experiencing rising total emissions due to expanding energy demand.
- Population dynamics significantly influence per-capita trends.
    """
)

# Display basic metrics
latest = global_agg[global_agg["year"] == global_agg["year"].max()].iloc[0]
col1, col2, col3 = st.columns(3)
col1.metric("Global CO₂ per capita (t/person)", f"{latest['co2_per_capita_global']:.2f}")
col2.metric("Global Renewable Share (%)", f"{latest['renewables_share_global']:.2f}")
col3.metric("Latest Year", int(latest["year"]))

st.markdown(
    """
### Notable Events
- 2008–2009: Global financial crisis influenced emissions and energy demand.
- 2015: Paris Agreement adoption; many NDCs accelerated renewable targets.
- 2020: COVID-19 shock led to a temporary emissions decline, followed by rebounds.

Note: Correlations between GDP growth and renewable adoption are descriptive, not causal.
    """
)

# Simple callout around the Paris Agreement
with st.expander("Context: Paris Agreement (2015)"):
    st.write(
        "Adopted in 2015, the Paris Agreement aims to limit global warming to well below 2°C."
        " Many countries ramped up renewable targets thereafter, though outcomes differ by policy, cost declines, and grid integration."
    )