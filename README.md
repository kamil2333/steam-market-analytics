# Steam Market Analytics

A data analytics and engineering portfolio project focused on exploring video game data from Steam.

The project demonstrates an end-to-end analytical workflow, covering raw data inspection, data cleaning, database design, data ingestion, SQL analysis, and interactive visualization using Power BI.

The main objective is to transform raw game data into structured, reliable datasets and derive meaningful insights about game prices, discounts, genres, and player popularity.

## Project Goals

- Inspect and assess raw dataset quality.
- Clean, transform, and validate data using Python and Pandas.
- Design and implement a relational data model in PostgreSQL.
- Build a structured data pipeline for database ingestion.
- Perform analytical queries using SQL.
- Develop interactive dashboards using Power BI and DAX.
- Explore statistical relationships and trends in the data.
- Document analytical findings and data limitations.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Data processing and ingestion |
| Pandas | Data cleaning and transformation |
| PostgreSQL | Relational database and data storage |
| SQL | Data modeling and analytical queries |
| Power BI | Interactive dashboards and visualization |
| DAX | Measures and analytical calculations |
| Git & GitHub | Version control and project management |

## Project Structure

```text
steam-game-analisys/
├── data/
│   ├── raw/
│   └── processed/
├── src/
│   └── inspect_data.py
├── sql/
│   ├── 01_create_raw_schema.sql
│   ├── 02_create_analytics_schema.sql
│   ├── 03_create_normalized_schema.sql
│   ├── 04_populate_normalized_tables.sql
│   └── analysis/
├── reports/
│   └── steam_market_analysis.pbix
├── .gitignore
├── README.md
└── requirements.txt
```

The `data/raw/` and `data/processed/` directories are excluded from version control where appropriate.

## Data Source

The project uses a publicly available Steam games dataset.

Source: [Steam Games Dataset – Zenodo](https://zenodo.org/records/15121027)

The dataset is not included in this repository. Its original snapshot is used for analytical purposes.

The results describe the collected dataset and should not be interpreted as current Steam prices, discounts, or review counts.

## Data Processing and Database Design

The data workflow consists of several stages:

1. **Raw data inspection** – examining dataset structure, data types, missing values, and inconsistencies.
2. **Data cleaning** – processing and validating raw data using Python and Pandas.
3. **Data ingestion** – loading processed data into PostgreSQL.
4. **Database modeling** – separating raw and analytical data into dedicated schemas.
5. **Normalization** – extracting genres and tags into relational tables to support more flexible analysis.
6. **SQL analysis** – investigating prices, discounts, reviews, genres, and other game attributes.
7. **Visualization** – connecting PostgreSQL to Power BI and building interactive reports.

## Power BI Dashboard

An interactive Power BI dashboard is being developed using data from the PostgreSQL analytical database.

The report currently contains two pages.

### 1. Overview

Provides a general overview of the dataset and game distribution.

Current visualizations include:
- Total number of games.
- Number of games with review data.
- Review data coverage.
- Average and median game prices.
- Top genres by number of games.
- Average game prices by genre.
- Top genres by total review count.
- Interactive genre and release year filters.

### 2. Pricing & Discounts

Focuses on pricing patterns and discount distribution.

Current visualizations include:
- Number of discounted games.
- Average discount percentage.
- Average original price of discounted games.
- Average price after discount.
- Distribution of games across discount ranges.
- Comparison of average and median review counts by discount range.
- Scatter plot showing the relationship between original price and discount percentage.

The report uses DAX measures and calculated columns to support dynamic calculations and interactive filtering.

### Planned Dashboard Pages

**3. Popularity & Reviews**
- Further analysis of positive and negative reviews.
- Game popularity comparisons.
- Review distribution and trends.
- Additional genre and release date analysis.

## Preliminary Analytical Findings

The following findings are based on the current dataset snapshot containing 2,927 Steam store items.

### Price Distribution

- Total dataset size: 2,927 items.
- 2,367 items have a recorded price.
- 560 items (19.13%) have missing prices.
- 188 items have a listed price of €0.
- Average recorded price: €15.89.
- Median recorded price: €10.35.

The difference between the average and median suggests that higher-priced games influence the overall average.

### Review Data

- 2,196 items have a recorded review count.
- 731 items have missing review counts.
- Counter-Strike 2 has the highest recorded review count in this historical dataset.
- Average review counts are substantially higher than medians in several discount categories, suggesting right-skewed distributions.

### Discount Analysis

- 641 items have a recorded discount.
- Average discount: 47.85%.
- Average original price of discounted games: €19.01.
- Average price after discount: €9.41.
- The most common discount range is 26–50%, covering 233 games (36.35% of discounted items).
- Discounts above 50% account for approximately 39.63% of discounted items.
- The average absolute difference between recorded and calculated discount percentages is 0.05 percentage points.
- No checked item exceeds the 1-percentage-point validation tolerance.

### Discount and Review Popularity

An exploratory comparison of average and median review counts across discount ranges revealed:

- Games with discounts of 51–75% have the highest average review count.
- Games with discounts of 76–100% have the highest median review count.
- The substantial difference between averages and medians indicates that highly reviewed games influence group averages.

These results show an association within the collected dataset, not a causal relationship between discounts and game popularity.

## Project Status

**In progress**

### Completed

- Raw data profiling and quality assessment.
- Data cleaning and transformation using Python and Pandas.
- Automated unit tests and data validation checks.
- PostgreSQL staging and analytical schemas.
- Python-based data ingestion into PostgreSQL.
- Normalized relational tables for genres and tags.
- Initial analytical SQL queries covering prices, reviews, discounts, genres, and tags.
- PostgreSQL connection to Power BI.
- Initial interactive Power BI dashboard with two report pages.

### In Progress

- Development of the Power BI dashboard.
- Further analytical SQL queries.
- Additional data quality investigation.
- Dashboard layout and visualization improvements.
- Documentation of analytical findings.

### Planned

- Complete the Popularity & Reviews dashboard page.
- Add further analytical visualizations.
- Improve dashboard design and usability.
- Add dashboard screenshots to the project documentation.
- Automate selected pipeline tasks through GitHub Actions.
- Evaluate potential machine learning applications based on the available data.

## Future Improvements

- Expand data quality checks.
- Improve pipeline automation and reproducibility.
- Extend analytical SQL queries.
- Explore additional statistical relationships.
- Improve dashboard interactivity and presentation.
- Document the complete data pipeline.
- Evaluate potential machine learning applications.

## Data Limitations

- The dataset represents a historical snapshot and does not reflect current Steam market conditions.
- Missing values are retained and are not automatically treated as zero.
- Review counts and discount information may be incomplete.
- Genre and tag assignments can overlap, meaning a single game may belong to multiple categories.
- Observational relationships should not be interpreted as evidence of causation.