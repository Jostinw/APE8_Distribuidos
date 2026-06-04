import socket
import threading
import time
import random
import json

# ── CONFIGURAR EN CADA PC ──────────────────────
MY_ID = 0           # 0=PC1, 1=PC2, 2=PC3, 3=PC4
MY_IP = '192.168.1.10'
PORT = 7000
N = 4               # número de PCs
# ──────────────────────────────────────────────

PEERS = {
    0: '192.168.1.10',
    1: '192.168.1.11',
    2: '192.168.1.12',
    3: '192.168.1.13',
}

vector_clock = [0] * N
lock = threading.Lock()
log = []

def local_event():
    with lock:
        vector_clock[MY_ID] += 1
        return list(vector_clock)

def send_message(dest_id, text):
    with lock:
        vector_clock[MY_ID] += 1
        vc_copy = list(vector_clock)
    msg = json.dumps({"src": MY_ID, "vc": vc_copy, "text": text})
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((PEERS[dest_id], PORT))
        s.sendall(msg.encode())
        s.close()
        entry = f"[SEND] PC{MY_ID}→PC{dest_id} | VC={vc_copy} | msg='{text}'"
        log.append(entry)
        print(entry)
    except Exception as e:
        print(f"[ERROR]: {e}")

def handle_client(conn):
    data = json.loads(conn.recv(4096).decode())
    conn.close()
    src_id = data["src"]
    recv_vc = data["vc"]
    text = data["text"]
    with lock:
        for i in range(N):
            vector_clock[i] = max(vector_clock[i], recv_vc[i])
        vector_clock[MY_ID] += 1
        vc_now = list(vector_clock)
    entry = f"[RECV] PC{src_id}→PC{MY_ID} | VC_recv={recv_vc} | VC_now={vc_now} | msg='{text}'"
    log.append(entry)
    print(entry)

def are_concurrent(vc1, vc2):
    less = any(vc1[i] < vc2[i] for i in range(N))
    greater = any(vc1[i] > vc2[i] for i in range(N))
    return less and greater

def server_thread():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((MY_IP, PORT))
    server.listen(10)
    while True:
        conn, _ = server.accept()
        threading.Thread(target=handle_client, args=(conn,)).start()

threading.Thread(target=server_thread, daemon=True).start()
print(f"[PC{MY_ID}] Vector Clock server iniciado. Esperando 3 segundos...")
time.sleep(3)

# Escenario de concurrencia:
# PC2 envía a PC3, mientras PC1 también envía a PC3 "simultáneamente"
destinos = [i for i in PEERS if i != MY_ID]
for dest in destinos[:2]:
    time.sleep(random.uniform(0.3, 1.0))
    send_message(dest, f"Evento de PC{MY_ID}")

time.sleep(4)
print(f"\n=== LOG FINAL PC{MY_ID} ===")
for entry in log:
    print(entry)
