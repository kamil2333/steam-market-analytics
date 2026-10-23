
import re
from collections.abc import Iterable
from typing import Any

import pandas as pd


REQUIRED_COLUMNS = {
    "price",
    "original_price",
    "discount",
    "reviews",
    "launch_date",
}

SPANISH_MONTHS = {
    "ENE": 1,
    "FEB": 2,
    "MAR": 3,
    "ABR": 4,
    "MAY": 5,
    "JUN": 6,
    "JUL": 7,
    "AGO": 8,
    "SEP": 9,
    "SEPT": 9,
    "SET": 9,
    "OCT": 10,
    "NOV": 11,
    "DIC": 12,
}


def _is_missing(value: Any) -> bool:
    """Return True when a scalar value is missing."""
    return value is None or bool(pd.isna(value))


def parse_price_eur(value: Any) -> float | None:
    """Convert a euro price string to a numeric value."""
    if _is_missing(value):
        return None

    text = str(value).strip()
    text = text.replace("€", "").replace("\u00a0", "")
    text = text.replace(" ", "")

    # Spanish-style prices use a comma as the decimal separator.
    if "," in text:
        text = text.replace(".", "").replace(",", ".")

    if not re.fullmatch(r"\d+(?:\.\d+)?", text):
        raise ValueError(f"Invalid euro price: {value!r}")

    return float(text)


def parse_discount_percent(value: Any) -> float | None:
    """Convert a discount such as '-77%' to a positive percentage."""
    if _is_missing(value):
        return None

    text = str(value).strip().replace("%", "").replace(" ", "")

    if "," in text:
        text = text.replace(".", "").replace(",", ".")

    try:
        percentage = abs(float(text))
    except ValueError as exc:
        raise ValueError(f"Invalid discount: {value!r}") from exc

    if not 0 <= percentage <= 100:
        raise ValueError(f"Discount is outside 0-100%: {value!r}")

    return percentage


def parse_review_count(value: Any) -> int | None:
    """Extract the number of user reviews from a localized string."""
    if _is_missing(value):
        return None

    text = str(value).strip()

    text = re.sub(
        r"\s*reseñas de usuarios\s*$",
        "",
        text,
        flags=re.IGNORECASE,
    )

    # In this dataset, periods are used as thousands separators.
    normalized = re.sub(r"[.,\s]", "", text)

    if not normalized.isdigit():
        raise ValueError(f"Invalid review count: {value!r}")

    return int(normalized)


def parse_spanish_date(value: Any) -> pd.Timestamp | None:
    """Parse a date containing a Spanish abbreviated month."""
    if _is_missing(value):
        return None

    text = re.sub(r"\s+", " ", str(value).strip().upper())
    parts = text.split(" ")

    if len(parts) != 3:
        raise ValueError(f"Invalid launch date: {value!r}")

    day_text, month_text, year_text = parts
    month_text = month_text.rstrip(".")

    if not day_text.isdigit() or not year_text.isdigit():
        raise ValueError(f"Invalid launch date: {value!r}")

    month = SPANISH_MONTHS.get(month_text)

    if month is None:
        raise ValueError(f"Unknown Spanish month in date: {value!r}")

    try:
        return pd.Timestamp(
            year=int(year_text),
            month=month,
            day=int(day_text),
        )
    except (ValueError, OverflowError) as exc:
        raise ValueError(f"Invalid calendar date: {value!r}") from exc


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add normalized columns while preserving the source columns.

    Invalid non-missing values raise ValueError instead of being
    silently converted to missing values.
    """
    missing_columns = REQUIRED_COLUMNS - set(df.columns)

    if missing_columns:
        names = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required columns: {names}")

    cleaned = df.copy()

    cleaned["price_eur"] = pd.Series(
        [parse_price_eur(value) for value in df["price"]],
        index=df.index,
        dtype="Float64",
    )

    cleaned["original_price_eur"] = pd.Series(
        [parse_price_eur(value) for value in df["original_price"]],
        index=df.index,
        dtype="Float64",
    )

    cleaned["discount_percent"] = pd.Series(
        [parse_discount_percent(value) for value in df["discount"]],
        index=df.index,
        dtype="Float64",
    )

    cleaned["review_count"] = pd.Series(
        [parse_review_count(value) for value in df["reviews"]],
        index=df.index,
        dtype="Int64",
    )

    cleaned["launch_date_parsed"] = pd.to_datetime(
        [parse_spanish_date(value) for value in df["launch_date"]]
    )

    return cleaned
