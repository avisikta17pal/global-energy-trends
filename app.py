from __future__ import annotations

import streamlit as st
import pandas as pd

from src.data_acquisition import load_raw_datasets
from src.data_processing import build_processed_dataset
from src.utils import ensure_directories, load_df


st.set_page_config(page_title="Global CO₂ & Renewables 1990–2023", page_icon="🌍", layout="wide")

@st.cache_data(show_spinner=True)
def get_data():
    ensure_directories()
    merged = load_df("merged.parquet")
    global_agg = load_df("global_aggregates.parquet")
    if merged is None or global_agg is None:
        co2, energy = load_raw_datasets()
        merged, global_agg = build_processed_dataset(co2, energy)
    return merged, global_agg

st.title("🌍 Global CO₂ Emissions and Renewable Energy Trends: 1990–2023")
st.markdown("Use the sidebar to navigate pages.")

try:
    with st.spinner("Preparing data..."):
        merged, global_agg = get_data()
    st.success("Data ready. Open pages from the sidebar.")
except Exception as exc:
    st.error(f"Failed to prepare data: {exc}")
    st.stop()