import pandas as pd

# Load raw traffic log
df = pd.read_csv("../data/traffic_log.csv")

# Convert timestamp to datetime object
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# Group by Source IP and compute features
grouped = df.groupby("Source IP").agg({
    "Packet Length": ["count", "mean", "max", "min"],
    "Protocol": lambda x: x.value_counts().to_dict()
})

# Flatten column names
grouped.columns = ['_'.join(col).strip() for col in grouped.columns.values]
grouped.reset_index(inplace=True)

# Save processed data
grouped.to_csv("../data/processed_dataset.csv", index=False)

print("✅ Feature extraction complete. Saved to data/processed_dataset.csv")
