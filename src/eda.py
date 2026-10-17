import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from src.preprocessing import load_data


def run_eda():
    df = load_data()

    print("Dataset shape:", df.shape)

    print("\nOperation modes:\n")
    print(df["Operation_Mode"].value_counts())

    print("\nEfficiency status:\n")
    print(df["Efficiency_Status"].value_counts())

    print("\nSensor statistics:\n")
    print(df.describe().round(2).to_string())

    output_dir = "data/processed"

    # 1. Distribution of mean machine temperatures
    df.groupby("Machine_ID")["Temperature_C"].mean().plot(
        kind="hist",
        bins=20,
        title="Distribution of Mean Machine Temperatures"
    )
    plt.xlabel("Mean Temperature (°C)")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/temperature_eda.png")
    plt.close()

    # 2. Sensor correlation heatmap
    numeric = df.select_dtypes(include="number")

    plt.figure(figsize=(12, 8))
    sns.heatmap(
        numeric.corr(),
        cmap="coolwarm",
        center=0,
        annot=False
    )
    plt.title("Sensor Correlation Heatmap")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/correlation_heatmap.png")
    plt.close()

    # 3. Efficiency status distribution
    df["Efficiency_Status"].value_counts().plot(
        kind="bar",
        title="Efficiency Status Distribution"
    )
    plt.xlabel("Efficiency Status")
    plt.ylabel("Number of Records")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/efficiency_distribution.png")
    plt.close()

    print("\nEDA completed successfully!")
    print("Charts saved in data/processed/")


if __name__ == "__main__":
    run_eda()