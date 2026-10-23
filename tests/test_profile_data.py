
import pandas as pd
import pytest

from src.profile_data import (
    build_column_profile,
    build_error_flag_profile,
    load_dataset,
)


def test_profile_reports_missing_values():
    df = pd.DataFrame(
        {
            "title": ["Game A", "Game B", "Game C"],
            "price": ["9,99€", None, None],
        }
    )

    profile = build_column_profile(df)
    price_profile = profile.loc[
        profile["column"] == "price"
    ].iloc[0]

    assert price_profile["non_null_count"] == 1
    assert price_profile["missing_count"] == 2
    assert price_profile["missing_percentage"] == 66.67
    assert price_profile["unique_count"] == 1


def test_profile_counts_unique_values():
    df = pd.DataFrame(
        {
            "title": ["Game A", "Game B", "Game A"],
        }
    )

    profile = build_column_profile(df)
    title_profile = profile.loc[
        profile["column"] == "title"
    ].iloc[0]

    assert title_profile["unique_count"] == 2


def test_load_dataset_reads_csv(tmp_path):
    csv_path = tmp_path / "sample.csv"

    pd.DataFrame(
        {
            "title": ["Game A", "Game B"],
            "price": [9.99, 19.99],
        }
    ).to_csv(csv_path, index=False)

    df = load_dataset(csv_path)

    assert df.shape == (2, 2)
    assert df["title"].tolist() == ["Game A", "Game B"]


def test_load_dataset_raises_when_file_does_not_exist(tmp_path):
    missing_path = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError, match="Dataset not found"):
        load_dataset(missing_path)


def test_error_flag_profile_reports_missing_metadata():
    df = pd.DataFrame(
        {
            "title": ["Game A", "Game B", "Game C"],
            "is_error": [0, 1, 1],
            "url": ["https://example.com/a", None, None],
            "tags": ["Action", None, None],
            "price": ["9,99€", None, None],
            "description": ["A game", None, None],
            "reviews": ["100 reviews", None, None],
        }
    )

    profile = build_error_flag_profile(df)
    error_rows = profile.loc[profile["is_error"] == 1].iloc[0]

    assert error_rows["record_count"] == 2
    assert error_rows["missing_url"] == 2
    assert error_rows["missing_tags"] == 2
    assert error_rows["missing_price"] == 2
    assert error_rows["missing_description"] == 2
    assert error_rows["missing_reviews"] == 2
