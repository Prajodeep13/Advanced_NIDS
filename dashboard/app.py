from flask import Flask, render_template
import pandas as pd
import ast
from collections import Counter

app = Flask(__name__)

def load_data():
    try:
        df = pd.read_csv("../data/processed_dataset.csv")
    except:
        return None

    data = {}

    # Label Distribution
    if "Label" in df.columns:
        label_counts = df["Label"].value_counts().to_dict()
        data["labels"] = {
            "Normal": label_counts.get(1, 0),
            "Attack": label_counts.get(0, 0)
        }

    # Top Source IPs
    if "Source IP" in df.columns:
        data["top_ips"] = df["Source IP"].value_counts().head(5).to_dict()

    # Protocol Count
    proto_counts = Counter()
    if "Protocol_<lambda>" in df.columns:
        for proto_json in df["Protocol_<lambda>"]:
            try:
                proto_dict = ast.literal_eval(proto_json)
                proto_counts.update(proto_dict)
            except:
                continue
        data["protocols"] = dict(proto_counts)

    return data

@app.route("/")
def index():
    data = load_data()
    return render_template("dashboard.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
