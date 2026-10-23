
import pandas as pd

from src.cleaning import clean_dataset
from src.validation import build_validation_report


def make_source(launch_date: str) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "title": ["Example Game"],
            "price": ["9,99€"],
            "original_price": ["19,99€"],
            "discount": ["-50%"],
            "reviews": ["1.234 reseñas de usuarios"],
            "launch_date": [launch_date],
        }
    )


def test_validation_passes_for_valid_data():
    source = make_source("9 DIC 2016")
    cleaned = clean_dataset(source)

    report = build_validation_report(source, cleaned)
    checks = report.set_index("check")

    assert checks.loc["row_count_preserved", "status"] == "PASS"
    assert checks.loc["source_columns_preserved", "status"] == "PASS"
    assert checks.loc["non_negative_prices", "status"] == "PASS"
    assert checks.loc["discounts_within_range", "status"] == "PASS"
    assert checks.loc["launch_date_intervals_ordered", "status"] == "PASS"
    assert checks.loc["date_precision_consistent", "status"] == "PASS"


def test_validation_warns_about_far_future_date():
    source = make_source("31 DIC 2099")
    cleaned = clean_dataset(source)

    report = build_validation_report(source, cleaned)
    checks = report.set_index("check")

    assert checks.loc["far_future_launch_dates", "status"] == "WARN"
    assert checks.loc["far_future_launch_dates", "issue_count"] == 1


def test_validation_reports_missing_prices_as_warning():
    source = make_source("9 DIC 2016")
    source.loc[0, "price"] = None

    cleaned = clean_dataset(source)
    report = build_validation_report(source, cleaned)
    checks = report.set_index("check")

    assert checks.loc["missing_prices", "status"] == "WARN"
    assert checks.loc["missing_prices", "issue_count"] == 1
