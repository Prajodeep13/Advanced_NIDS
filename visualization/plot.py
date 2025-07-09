import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import ast

# Load processed dataset
df = pd.read_csv("../data/processed_dataset.csv")

# Load label if exists
if "Label" in df.columns:
    label_counts = df["Label"].value_counts()
    label_counts.index = ["Attack" if i == 0 else "Normal" for i in label_counts.index]
    
    plt.figure(figsize=(6, 4))
    plt.title("Traffic Classification (Attack vs Normal)")
    plt.pie(label_counts, labels=label_counts.index, autopct='%1.1f%%', startangle=140, colors=["red", "green"])
    plt.axis("equal")
    plt.show()

# Top Talkers
if "Source IP" in df.columns:
    top_ips = df["Source IP"].value_counts().head(5)
    
    plt.figure(figsize=(8, 4))
    plt.title("Top 5 Source IPs")
    top_ips.plot(kind="bar", color="steelblue")
    plt.xlabel("Source IP")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.show()

# Protocol Distribution (from protocol JSON)
if "Protocol_<lambda>" in df.columns:
    proto_counts = Counter()
    for proto_json in df["Protocol_<lambda>"]:
        try:
            proto_dict = ast.literal_eval(proto_json)
            proto_counts.update(proto_dict)
        except:
            continue

    if proto_counts:
        plt.figure(figsize=(6, 4))
        plt.title("Protocol Usage Distribution")
        plt.bar(proto_counts.keys(), proto_counts.values(), color="purple")
        plt.xlabel("Protocol")
        plt.ylabel("Packet Count")
        plt.tight_layout()
        plt.show()
