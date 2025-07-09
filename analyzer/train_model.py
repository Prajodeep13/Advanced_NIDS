import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
import joblib
import ast

# Load processed dataset
df = pd.read_csv("../data/processed_dataset.csv")

# Clean and prepare protocol dictionary into separate columns
def decode_protocols(proto_str):
    proto_dict = ast.literal_eval(proto_str) if isinstance(proto_str, str) else {}
    return pd.Series({
        "TCP_Count": proto_dict.get("TCP", 0),
        "UDP_Count": proto_dict.get("UDP", 0),
        "Other_Count": proto_dict.get("Other", 0)
    })

proto_df = df["Protocol_<lambda>"].apply(decode_protocols)
df = pd.concat([df.drop("Protocol_<lambda>", axis=1), proto_df], axis=1)

# Load or add labels manually
# For demo, randomly assign labels (you should replace this with real labels)
import numpy as np
df["Label"] = np.random.choice(["Normal", "Attack"], size=len(df), p=[0.8, 0.2])

# Encode labels
label_encoder = LabelEncoder()
df["Label"] = label_encoder.fit_transform(df["Label"])  # 0 = Attack, 1 = Normal

# Feature set and target
X = df.drop(["Source IP", "Label"], axis=1)
y = df["Label"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
print("✅ Model Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(clf, "../models/nids_model.pkl")
print("✅ Model saved as models/nids_model.pkl")
