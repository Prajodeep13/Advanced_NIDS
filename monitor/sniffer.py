from scapy.all import sniff, IP, TCP, UDP
import csv
from datetime import datetime

# CSV file to store captured packet info
output_file = "../data/traffic_log.csv"

# Write CSV header
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "Source IP", "Destination IP", "Protocol", "Packet Length"])

def process_packet(packet):
    if IP in packet:
        ip_layer = packet[IP]
        protocol = "Other"

        if TCP in packet:
            protocol = "TCP"
        elif UDP in packet:
            protocol = "UDP"

        with open(output_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                ip_layer.src,
                ip_layer.dst,
                protocol,
                len(packet)
            ])
        print(f"[{protocol}] {ip_layer.src} → {ip_layer.dst} ({len(packet)} bytes)")

print("🚦 Starting packet capture... Press Ctrl+C to stop.")
sniff(prn=process_packet, store=False)
