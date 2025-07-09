🛡️ Advanced Network Intrusion Detection System (NIDS) Using Machine Learning
A real-time, modular Network Intrusion Detection System (NIDS) built using Python. This system captures live network packets, extracts traffic features, applies a machine learning model to detect attacks, and provides visual insights through an interactive Flask web dashboard.

📌 Features
📡 Live Packet Capture via Scapy

🧠 Machine Learning-based Threat Detection

📊 Protocol and IP-level Visualization

🖥️ Web-based Dashboard (Auto-Refreshing)

💾 Offline Visualization Support

⚙️ Modular, Scalable Codebase


🧠 How It Works
Packet Capture: Collects network traffic and logs source IP, protocol, and size.

Feature Extraction: Aggregates data per IP and creates a feature-rich dataset.

Model Training: Trains a Random Forest classifier to detect Attack vs Normal.

Real-Time Detection: Applies the model live and prints alerts to the console.

Visualization: Provides charts and IP usage summaries.

Dashboard: A Flask app displays results in a live auto-refresh dashboard.



Requirements

Step 1 : Capture Packets
python monitor/sniffer.py

Step 2 : Feature Extraction
python analyzer/extract_features.py

Step 3 : Train ML Model
python analyzer/train_model.py

step 4 : Real time detection
python analyzer/detect_lie.py

Step 5 : View Dashboard
python dashboard/app.py

Step 6 : View offline charts
python visualization/plot.py
