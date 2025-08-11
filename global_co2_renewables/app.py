from __future__ import annotations

import streamlit as st
import pandas as pd

from src.data_processing import compute_global_aggregates
from src.utils import ensure_directories, load_df, PROCESSED_DIR, validate_merged_schema, required_merged_columns


st.set_page_config(page_title="Global CO₂ & Renewables 1990–2023", page_icon="🌍", layout="wide")

@st.cache_data(show_spinner=True)
def get_data():
    ensure_directories()
    merged = load_df("merged.parquet")
    global_agg = load_df("global_aggregates.parquet")
    return merged, global_agg

st.title("🌍 Global CO₂ Emissions and Renewable Energy Trends: 1990–2023")
st.markdown("Use the sidebar to upload data and navigate pages.")

with st.sidebar:
    st.subheader("Data source")
    st.caption("Upload your processed CSVs to use the app offline.")
    with st.expander("Expected columns"):
        st.code("\n".join(required_merged_columns()))
        st.download_button(
            label="Download template (CSV headers)",
            data=(",".join(required_merged_columns()) + "\n").encode("utf-8"),
            file_name="merged_template.csv",
            mime="text/csv",
        )
    uploaded_merged = st.file_uploader("Upload merged dataset (CSV)", type=["csv"], key="merged_csv")
    uploaded_global = st.file_uploader("Upload global aggregates (CSV, optional)", type=["csv"], key="global_csv")
    if uploaded_merged is not None:
        ensure_directories()
        PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
        merged_path = PROCESSED_DIR / "merged.csv"
        merged_path.write_bytes(uploaded_merged.read())
        try:
            df_merged = pd.read_csv(merged_path)
            ok, missing = validate_merged_schema(df_merged)
            if not ok:
                st.error(f"Uploaded merged CSV is missing required columns: {missing}")
            else:
                if uploaded_global is not None:
                    (PROCESSED_DIR / "global_aggregates.csv").write_bytes(uploaded_global.read())
                else:
                    df_global = compute_global_aggregates(df_merged)
                    df_global.to_csv(PROCESSED_DIR / "global_aggregates.csv", index=False)
                get_data.clear()
                st.success("Uploaded data saved. The app will use it now.")
                st.experimental_rerun()
        except Exception as e:
            st.error(f"Could not read or process uploaded CSV: {e}")

try:
    with st.spinner("Loading data..."):
        merged, global_agg = get_data()
    if merged is None or global_agg is None:
        st.info("No local data found. Please upload processed CSVs via the sidebar to proceed.")
        st.stop()
    st.success("Data ready. Open pages from the sidebar.")
except Exception as exc:
    st.error(f"Failed to load data: {exc}")
    st.stop()