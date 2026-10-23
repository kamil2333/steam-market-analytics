
import calendar
import re
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

SPANISH_FULL_MONTHS = {
    "ENERO": 1,
    "FEBRERO": 2,
    "MARZO": 3,
    "ABRIL": 4,
    "MAYO": 5,
    "JUNIO": 6,
    "JULIO": 7,
    "AGOSTO": 8,
    "SEPTIEMBRE": 9,
    "SETIEMBRE": 9,
    "OCTUBRE": 10,
    "NOVIEMBRE": 11,
    "DICIEMBRE": 12,
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

    normalized = re.sub(r"[.,\s]", "", text)

    if not normalized.isdigit():
        raise ValueError(f"Invalid review count: {value!r}")

    return int(normalized)


def parse_spanish_date(value: Any) -> pd.Timestamp | None:
    """Parse an exact date containing a Spanish abbreviated month."""
    if _is_missing(value):
        return None

    text = re.sub(r"\s+", " ", str(value).strip().upper())

    match = re.fullmatch(
        r"(\d{1,2})\s+([A-ZÁÉÍÓÚÜÑ.]+)\s+(\d{4})",
        text,
    )

    if not match:
        raise ValueError(f"Invalid exact launch date: {value!r}")

    day_text, month_text, year_text = match.groups()
    month_text = month_text.rstrip(".")

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


def _date_interval(
    year: int,
    start_month: int,
    end_month: int,
    precision: str,
) -> dict[str, pd.Timestamp | str | None]:
    """Build a calendar interval for an imprecise launch date."""
    start = pd.Timestamp(year=year, month=start_month, day=1)

    last_day = calendar.monthrange(year, end_month)[1]
    end = pd.Timestamp(year=year, month=end_month, day=last_day)

    return {
        "start": start,
        "end": end,
        "precision": precision,
    }


def parse_launch_date(
    value: Any,
) -> dict[str, pd.Timestamp | str | None]:
    """
    Parse exact and imprecise launch dates.

    The result contains the earliest possible date, the latest possible
    date, and the precision of the source value. A coming-soon entry
    has unknown date bounds, while a missing source value is marked
    separately.
    """
    if _is_missing(value):
        return {
            "start": None,
            "end": None,
            "precision": "missing",
        }

    text = re.sub(r"\s+", " ", str(value).strip().upper())

    if not text:
        return {
            "start": None,
            "end": None,
            "precision": "missing",
        }

    if text in {"PRÓXIMAMENTE", "PROXIMAMENTE"}:
        return {
            "start": None,
            "end": None,
            "precision": "coming_soon",
        }

    # Year only, for example: 2025
    if re.fullmatch(r"\d{4}", text):
        year = int(text)
        return _date_interval(year, 1, 12, "year")

    # Quarter, for example:
    # 4.º TRIMESTRE DEL 2028
    # 1.ᵉʳ TRIMESTRE DEL 2026
    quarter_match = re.fullmatch(
        r"([1-4])\..*?\s+TRIMESTRE\s+DEL\s+(\d{4})",
        text,
    )

    if quarter_match:
        quarter = int(quarter_match.group(1))
        year = int(quarter_match.group(2))
        start_month = (quarter - 1) * 3 + 1
        end_month = start_month + 2

        return _date_interval(
            year,
            start_month,
            end_month,
            "quarter",
        )

    # Month and year, for example: SEPTIEMBRE DE 2025
    month_match = re.fullmatch(
        r"([A-ZÁÉÍÓÚÜÑ]+)\s+DE\s+(\d{4})",
        text,
    )

    if month_match:
        month_name = month_match.group(1)
        year = int(month_match.group(2))
        month = SPANISH_FULL_MONTHS.get(month_name)

        if month is None:
            raise ValueError(f"Unknown Spanish month: {value!r}")

        return _date_interval(year, month, month, "month")

    # Exact day, for example: 9 DIC 2016
    try:
        exact_date = parse_spanish_date(text)
    except ValueError as exc:
        raise ValueError(f"Unsupported launch date: {value!r}") from exc

    if exact_date is None:
        return {
            "start": None,
            "end": None,
            "precision": "missing",
        }

    return {
        "start": exact_date,
        "end": exact_date,
        "precision": "day",
    }


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add normalized columns while preserving the source columns.

    Invalid non-missing values raise ValueError rather than being
    silently discarded.
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

    date_results = [
        parse_launch_date(value)
        for value in df["launch_date"]
    ]

    cleaned["launch_date_start"] = pd.to_datetime(
        [result["start"] for result in date_results]
    )

    cleaned["launch_date_end"] = pd.to_datetime(
        [result["end"] for result in date_results]
    )

    cleaned["launch_date_precision"] = [
        result["precision"] for result in date_results
    ]

    # This column contains a date only when the source specifies
    # an exact day. It must not imply false precision.
    cleaned["launch_date_parsed"] = pd.to_datetime(
        [
            result["start"]
            if result["precision"] == "day"
            else None
            for result in date_results
        ]
    )

    return cleaned
