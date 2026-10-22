
from pathlib import Path

import pandas as pd


DATA_PATH = Path("data/raw/steam-games.csv")


def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Nie znaleziono pliku: {DATA_PATH.resolve()}"
        )

    # Wczytanie danych z pliku CSV
    df = pd.read_csv(DATA_PATH)

    # Podstawowe informacje o zbiorze
    print("ROZMIAR DANYCH")
    print(f"Liczba wierszy: {df.shape[0]}")
    print(f"Liczba kolumn: {df.shape[1]}")

    print("\nNAZWY KOLUMN")
    print(df.columns.tolist())

    print("\nPIERWSZE 5 REKORDÓW")
    print(df.head().to_string(index=False))

    print("\nTYPY DANYCH I LICZBA NIEPUSTYCH WARTOŚCI")
    df.info()

    print("\nBRAKUJĄCE WARTOŚCI")
    print(df.isna().sum().sort_values(ascending=False))

    print("\nLICZBA DUPLIKATÓW")
    print(df.duplicated().sum())


if __name__ == "__main__":
    main()
