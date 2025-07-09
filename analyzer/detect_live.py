from scapy.all import sniff, IP, TCP, UDP
from datetime import datetime
import pandas as pd
import joblib
import ast
import os
# Load trained model
model = joblib.load("../models/nids_model.pkl")
print("✅ Model loaded successfully")

# Track stats per IP
ip_stats = {}

def extract_features(ip):
    stats = ip_stats.get(ip, {"count": 0, "total_len": 0, "tcp": 0, "udp": 0})
    avg_len = stats["total_len"] / stats["count"] if stats["count"] > 0 else 0
    return pd.DataFrame([{
        "Packet Length_count": stats["count"],
        "Packet Length_mean": avg_len,
        "Packet Length_max": stats.get("max_len", 0),
        "Packet Length_min": stats.get("min_len", 0),
        "TCP_Count": stats["tcp"],
        "UDP_Count": stats["udp"],
        "Other_Count": stats["count"] - stats["tcp"] - stats["udp"]
    }])

def process_packet(packet):
    if IP in packet:
        ip_layer = packet[IP]
        proto = "Other"
        if TCP in packet:
            proto = "TCP"
        elif UDP in packet:
            proto = "UDP"

        src_ip = ip_layer.src
        pkt_len = len(packet)

        if src_ip not in ip_stats:
            ip_stats[src_ip] = {
                "count": 0, "total_len": 0,
                "tcp": 0, "udp": 0,
                "max_len": pkt_len,
                "min_len": pkt_len
            }

        stats = ip_stats[src_ip]
        stats["count"] += 1
        stats["total_len"] += pkt_len
        stats["max_len"] = max(stats["max_len"], pkt_len)
        stats["min_len"] = min(stats["min_len"], pkt_len)
        if proto == "TCP":
            stats["tcp"] += 1
        elif proto == "UDP":
            stats["udp"] += 1

        # Feature extraction
        features = extract_features(src_ip)

        # Predict
        prediction = model.predict(features)[0]
        label = "Normal" if prediction == 1 else "⚠️ Attack"

        print(f"[{label}] {src_ip} ({proto}, {pkt_len} bytes)")

print("🚨 Real-time detection started... Press Ctrl+C to stop.")
sniff(prn=process_packet, store=False)
