
# Steam Market Analytics

A data analytics and engineering project focused on exploring video game data from Steam.

The project is designed to demonstrate a complete data workflow, from raw data inspection and cleaning to database storage, SQL analysis, and interactive visualization.

## Project Goals

- Inspect and assess raw data quality.
- Clean and validate data using Python and Pandas.
- Store structured data in PostgreSQL.
- Perform analytical queries using SQL.
- Build an interactive Power BI dashboard.
- Explore statistical relationships in the data.
- Optionally develop a machine learning component.

## Tech Stack

- Python
- Pandas
- SQL
- PostgreSQL
- Git and GitHub
- Power BI (planned)

## Project Structure

```text
steam-game-analisys/
├── data/
│   ├── raw/
│   └── processed/
├── src/
│   └── inspect_data.py
├── .gitignore
├── README.md
└── requirements.txt
```

## Getting Started

### Requirements

- Python 3.11 or newer
- Git

### Setup

Clone the repository and enter the project directory:

```bash
git clone <repository-url>
cd steam-game-analisys
```

Create and activate a virtual environment.

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Place the source CSV file in `data/raw/steam-games.csv`.

Run the initial data inspection:

```bash
python src/inspect_data.py
```

## Data Source

The project uses a publicly available Steam games dataset.

Source: https://zenodo.org/records/15121027

The dataset is not included in this repository. Its exact version, provenance, and applicable usage terms will be verified and documented before the data pipeline is finalized.

## Project Status

**In progress** — initial repository setup and raw data inspection.

## Future Improvements

- Data cleaning and validation
- Automated tests
- PostgreSQL schema and data loading
- SQL analytical queries
- Data quality checks
- Power BI dashboard
- Automated pipeline execution
- Optional machine learning experiments
