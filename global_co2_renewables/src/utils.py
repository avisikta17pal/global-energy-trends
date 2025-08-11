"""Utility helpers for paths, constants, and common operations."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
ASSETS_DIR = PROJECT_ROOT / "assets"
SCREENSHOTS_DIR = ASSETS_DIR / "screenshots"


@dataclass(frozen=True)
class Constants:
    start_year: int = 1990
    end_year: int = 2023
    # Paris Agreement year for context
    paris_agreement_year: int = 2015


def ensure_directories() -> None:
    for p in [DATA_DIR, RAW_DIR, PROCESSED_DIR, ASSETS_DIR, SCREENSHOTS_DIR]:
        p.mkdir(parents=True, exist_ok=True)


def standardize_countries(df: pd.DataFrame, country_col: str = "country") -> pd.DataFrame:
    """Standardize country names while preserving existing iso_code from OWID.

    - If `iso_code` exists, keep it for matching and maps.
    - Use `country_converter` (if available) to fill missing iso codes and to create a
      standardized `country_standard` name column.
    - On failure, keep original names and add placeholders.
    """
    df = df.copy()
    if "iso_code" not in df.columns:
        df["iso_code"] = pd.NA

    try:
        import country_converter as coco

        cc = coco.CountryConverter()
        # Create standardized names based on provided country names
        name_short = cc.convert(names=df[country_col].tolist(), to="name_short")
        # Only fill iso codes where missing
        iso3_conv = cc.convert(names=df[country_col].tolist(), to="ISO3")
        df["country_standard"] = name_short
        # Fill iso_code only when missing and converter result is valid
        mask_missing_iso = df["iso_code"].isna()
        iso3_series = pd.Series(iso3_conv, index=df.index)
        df.loc[mask_missing_iso & (~iso3_series.isin(["not found", None])), "iso_code"] = iso3_series
        # Fallback to original country if converter failed
        df["country_standard"].fillna(df[country_col], inplace=True)
        return df
    except Exception:
        if "country_standard" not in df.columns:
            df["country_standard"] = df[country_col]
        return df


def add_continent(df: pd.DataFrame, iso_col: str = "iso_code") -> pd.DataFrame:
    """Add continent classification, using country_converter if available."""
    try:
        import country_converter as coco

        cc = coco.CountryConverter()
        continents = cc.convert(names=df[iso_col].tolist(), to="continent")
        df = df.assign(continent=continents)
        df.loc[df["continent"].isin(["not found", None]), "continent"] = pd.NA
        return df
    except Exception:
        if "continent" not in df.columns:
            df = df.copy()
            df["continent"] = pd.NA
        return df


def save_df(df: pd.DataFrame, name: str) -> Path:
    path = PROCESSED_DIR / name
    df.to_parquet(path, index=False)
    return path


def load_df(name: str) -> Optional[pd.DataFrame]:
    path = PROCESSED_DIR / name
    if path.exists():
        return pd.read_parquet(path)
    return None