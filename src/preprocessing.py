import pandas as pd
from pathlib import Path


def load_data():
    path = Path("data/raw/Thales_Group_Manufacturing.csv")
    df = pd.read_csv(path)

    df["Datetime"] = pd.to_datetime(
        df["Date"] + " " + df["Timestamp"],
        format="%d-%m-%Y %H:%M:%S"
    )

    df = df.sort_values(["Machine_ID", "Datetime"])
    df = df.drop_duplicates(
        subset=["Machine_ID", "Datetime"]
    )

    return df.reset_index(drop=True)


if __name__ == "__main__":
    df = load_data()
    print("Dataset shape:", df.shape)
    print("Machines:", df["Machine_ID"].nunique())
    print("Date range:", df["Datetime"].min(), "to", df["Datetime"].max())
    print("\nData types:\n", df.dtypes)
    print("\nSample:\n", df.head(3).to_string(index=False))