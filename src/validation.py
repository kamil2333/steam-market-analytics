
import pandas as pd


FAR_FUTURE_REVIEW_THRESHOLD = pd.Timestamp("2050-01-01")


def build_validation_report(
    source: pd.DataFrame,
    cleaned: pd.DataFrame,
) -> pd.DataFrame:
    """Validate the cleaned dataset and report potential issues."""
    results = []

    def add_check(
        name: str,
        issue_count: int,
        details: str,
        warning_only: bool = False,
    ) -> None:
        if issue_count == 0:
            status = "PASS"
        elif warning_only:
            status = "WARN"
        else:
            status = "FAIL"

        results.append(
            {
                "check": name,
                "status": status,
                "issue_count": int(issue_count),
                "details": details,
            }
        )

    # 1. The cleaning process must not drop or add records.
    row_difference = abs(len(source) - len(cleaned))

    add_check(
        "row_count_preserved",
        row_difference,
        f"Source: {len(source)}, cleaned: {len(cleaned)}",
    )

    # 2. Original columns and their values must remain unchanged.
    changed_columns = [
        column
        for column in source.columns
        if column not in cleaned.columns
        or not source[column].equals(cleaned[column])
    ]

    add_check(
        "source_columns_preserved",
        len(changed_columns),
        (
            "All original columns and values are preserved."
            if not changed_columns
            else f"Changed or missing columns: {changed_columns}"
        ),
    )

    # 3. Prices must not be negative.
    negative_prices = int((cleaned["price_eur"].dropna() < 0).sum())

    add_check(
        "non_negative_prices",
        negative_prices,
        "Normalized game prices must be zero or greater.",
    )

    # 4. Discounts must be between 0 and 100 percent.
    discounts = cleaned["discount_percent"].dropna()

    invalid_discounts = int(
        ((discounts < 0) | (discounts > 100)).sum()
    )

    add_check(
        "discounts_within_range",
        invalid_discounts,
        "Normalized discounts must be between 0 and 100.",
    )

    # 5. Date intervals must not be reversed.
    start_dates = cleaned["launch_date_start"]
    end_dates = cleaned["launch_date_end"]

    comparable_dates = start_dates.notna() & end_dates.notna()
    reversed_intervals = comparable_dates & (start_dates > end_dates)

    add_check(
        "launch_date_intervals_ordered",
        int(reversed_intervals.sum()),
        "A launch date interval must start before or on its end date.",
    )

    # 6. Only exact-day dates should populate launch_date_parsed.
    precision = cleaned["launch_date_precision"]
    parsed_dates = cleaned["launch_date_parsed"]

    exact_day = precision.eq("day")

    inconsistent_dates = (
        exact_day
        & (
            parsed_dates.isna()
            | parsed_dates.ne(start_dates)
            | parsed_dates.ne(end_dates)
        )
    ) | (~exact_day & parsed_dates.notna())

    add_check(
        "date_precision_consistent",
        int(inconsistent_dates.sum()),
        "Exact-day dates must match both interval boundaries.",
    )

    # 7. Missing data are reported as warnings, not automatic failures.
    missing_prices = int(cleaned["price_eur"].isna().sum())

    add_check(
        "missing_prices",
        missing_prices,
        "Missing prices are retained and require context before analysis.",
        warning_only=True,
    )

    missing_reviews = int(cleaned["review_count"].isna().sum())

    add_check(
        "missing_review_counts",
        missing_reviews,
        "Missing review counts are retained.",
        warning_only=True,
    )

    # 8. Extremely distant dates need review, but are not changed.
    far_future = (
        cleaned["launch_date_start"]
        >= FAR_FUTURE_REVIEW_THRESHOLD
    ).fillna(False)

    suspicious_titles = cleaned.loc[far_future, "title"].astype(str)

    add_check(
        "far_future_launch_dates",
        int(far_future.sum()),
        (
            "No dates meet the review threshold."
            if not far_future.any()
            else (
                "Review dates from "
                f"{FAR_FUTURE_REVIEW_THRESHOLD.date()} onward: "
                + ", ".join(suspicious_titles)
            )
        ),
        warning_only=True,
    )

    return pd.DataFrame(results)
