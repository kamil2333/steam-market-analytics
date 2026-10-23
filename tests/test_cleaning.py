
import pandas as pd
import pytest

from src.cleaning import (
    clean_dataset,
    parse_discount_percent,
    parse_launch_date,
    parse_price_eur,
    parse_review_count,
    parse_spanish_date,
)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("9,75€", 9.75),
        ("0€", 0.0),
        ("1.234,56€", 1234.56),
    ],
)
def test_parse_price_eur(value, expected):
    assert parse_price_eur(value) == pytest.approx(expected)


@pytest.mark.parametrize("value", [None, pd.NA, float("nan")])
def test_parse_price_eur_handles_missing_values(value):
    assert parse_price_eur(value) is None


def test_parse_price_eur_rejects_invalid_value():
    with pytest.raises(ValueError, match="Invalid euro price"):
        parse_price_eur("not a price")


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("-77%", 77.0),
        ("-8%", 8.0),
        ("0%", 0.0),
    ],
)
def test_parse_discount_percent(value, expected):
    assert parse_discount_percent(value) == pytest.approx(expected)


def test_parse_discount_percent_handles_missing_value():
    assert parse_discount_percent(None) is None


def test_parse_discount_percent_rejects_invalid_percentage():
    with pytest.raises(ValueError, match="outside 0-100"):
        parse_discount_percent("-120%")


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("63.401 reseñas de usuarios", 63401),
        ("8.679.136 reseñas de usuarios", 8679136),
        ("2748 reseñas de usuarios", 2748),
    ],
)
def test_parse_review_count(value, expected):
    assert parse_review_count(value) == expected


def test_parse_review_count_handles_missing_value():
    assert parse_review_count(None) is None


def test_parse_review_count_rejects_invalid_value():
    with pytest.raises(ValueError, match="Invalid review count"):
        parse_review_count("many reviews")


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("9 DIC 2016", pd.Timestamp("2016-12-09")),
        ("30 MAY 2013", pd.Timestamp("2013-05-30")),
        ("5 SEPT 2022", pd.Timestamp("2022-09-05")),
        ("31 DIC 2096", pd.Timestamp("2096-12-31")),
    ],
)
def test_parse_spanish_date(value, expected):
    assert parse_spanish_date(value) == expected


def test_parse_spanish_date_handles_missing_value():
    assert parse_spanish_date(None) is None


def test_parse_spanish_date_rejects_unknown_month():
    with pytest.raises(ValueError, match="Unknown Spanish month"):
        parse_spanish_date("10 XYZ 2020")


def test_clean_dataset_preserves_source_columns():
    source = pd.DataFrame(
        {
            "price": ["9,75€", None],
            "original_price": ["19,50€", None],
            "discount": ["-50%", None],
            "reviews": ["1.234 reseñas de usuarios", None],
            "launch_date": ["9 DIC 2016", None],
        }
    )

    cleaned = clean_dataset(source)

    assert cleaned.loc[0, "price"] == "9,75€"
    assert cleaned.loc[0, "price_eur"] == pytest.approx(9.75)
    assert cleaned.loc[0, "discount_percent"] == pytest.approx(50)
    assert cleaned.loc[0, "review_count"] == 1234
    assert cleaned.loc[0, "launch_date_parsed"] == pd.Timestamp(
        "2016-12-09"
    )

    assert pd.isna(cleaned.loc[1, "price_eur"])
    assert pd.isna(cleaned.loc[1, "review_count"])
    assert pd.isna(cleaned.loc[1, "launch_date_parsed"])

    assert "price" in cleaned.columns
    assert "reviews" in cleaned.columns

 
@pytest.mark.parametrize(
    ("value", "expected_start", "expected_end", "precision"),
    [
        (
            "2025",
            "2025-01-01",
            "2025-12-31",
            "year",
        ),
        (
            "4.º TRIMESTRE DEL 2028",
            "2028-10-01",
            "2028-12-31",
            "quarter",
        ),
        (
            "1.ᵉʳ TRIMESTRE DEL 2026",
            "2026-01-01",
            "2026-03-31",
            "quarter",
        ),
        (
            "SEPTIEMBRE DE 2025",
            "2025-09-01",
            "2025-09-30",
            "month",
        ),
        (
            "FEBRERO DE 2026",
            "2026-02-01",
            "2026-02-28",
            "month",
        ),
        (
            "9 DIC 2016",
            "2016-12-09",
            "2016-12-09",
            "day",
        ),
        (
            "PRÓXIMAMENTE",
            None,
            None,
            "coming_soon",
        ),
        (
            None,
            None,
            None,
            "missing",
        ),
    ],
)
def test_parse_launch_date(
    value,
    expected_start,
    expected_end,
    precision,
):
    result = parse_launch_date(value)

    expected_start = (
        pd.Timestamp(expected_start)
        if expected_start is not None
        else None
    )
    expected_end = (
        pd.Timestamp(expected_end)
        if expected_end is not None
        else None
    )

    assert result["start"] == expected_start
    assert result["end"] == expected_end
    assert result["precision"] == precision


def test_clean_dataset_preserves_imprecise_launch_date():
    source = pd.DataFrame(
        {
            "price": ["9,75€"],
            "original_price": ["19,50€"],
            "discount": ["-50%"],
            "reviews": ["1.234 reseñas de usuarios"],
            "launch_date": ["4.º TRIMESTRE DEL 2028"],
        }
    )

    cleaned = clean_dataset(source)

    assert cleaned.loc[0, "launch_date_start"] == pd.Timestamp(
        "2028-10-01"
    )
    assert cleaned.loc[0, "launch_date_end"] == pd.Timestamp(
        "2028-12-31"
    )
    assert cleaned.loc[0, "launch_date_precision"] == "quarter"
    assert pd.isna(cleaned.loc[0, "launch_date_parsed"])
    assert cleaned.loc[0, "launch_date"] == "4.º TRIMESTRE DEL 2028"
