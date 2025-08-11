"""Data acquisition: download OWID CO2 and Energy datasets and cache locally."""
from __future__ import annotations

import io
from pathlib import Path
from typing import Tuple

import pandas as pd
import requests

from .utils import RAW_DIR, ensure_directories


OWID_CO2_URL = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
OWID_ENERGY_URL = "https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv"
HEADERS = {"User-Agent": "global-co2-renewables/1.0"}


def _download_csv(url: str) -> pd.DataFrame:
    try:
        response = requests.get(url, timeout=60, headers=HEADERS)
        response.raise_for_status()
        return pd.read_csv(io.StringIO(response.text))
    except Exception as exc:
        raise RuntimeError(f"Failed to download dataset from {url}: {exc}") from exc


def download_owid_datasets(force: bool = False) -> Tuple[Path, Path]:
    """Download CO2 and Energy datasets to RAW_DIR; return paths."""
    ensure_directories()
    co2_path = RAW_DIR / "owid-co2-data.csv"
    energy_path = RAW_DIR / "owid-energy-data.csv"

    if force or not co2_path.exists():
        co2_df = _download_csv(OWID_CO2_URL)
        co2_df.to_csv(co2_path, index=False)
    if force or not energy_path.exists():
        energy_df = _download_csv(OWID_ENERGY_URL)
        energy_df.to_csv(energy_path, index=False)

    return co2_path, energy_path


def load_raw_datasets() -> Tuple[pd.DataFrame, pd.DataFrame]:
    co2_path, energy_path = download_owid_datasets(force=False)
    co2 = pd.read_csv(co2_path)
    energy = pd.read_csv(energy_path)
    return co2, energy