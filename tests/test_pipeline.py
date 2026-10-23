
import pandas as pd

from src.run_pipeline import run_pipeline


def test_pipeline_exports_cleaned_data_and_validation_report(tmp_path):
    source_path = tmp_path / "source.csv"
    output_dir = tmp_path / "processed"

    source = pd.DataFrame(
        {
            "title": ["Example Game"],
            "price": ["9,99€"],
            "original_price": ["19,99€"],
            "discount": ["-50%"],
            "reviews": ["1.234 reseñas de usuarios"],
            "launch_date": ["9 DIC 2016"],
        }
    )

    source.to_csv(source_path, index=False)

    report = run_pipeline(source_path, output_dir)

    cleaned_path = output_dir / "steam-games-cleaned.csv"
    report_path = output_dir / "validation-report.csv"

    assert cleaned_path.exists()
    assert report_path.exists()
    assert not (report["status"] == "FAIL").any()

    cleaned = pd.read_csv(cleaned_path)

    assert len(cleaned) == 1
    assert cleaned.loc[0, "price_eur"] == 9.99
    assert cleaned.loc[0, "review_count"] == 1234
    assert cleaned.loc[0, "launch_date_precision"] == "day"

    # Original source values must remain available.
    assert cleaned.loc[0, "price"] == "9,99€"
    assert cleaned.loc[0, "launch_date"] == "9 DIC 2016"
