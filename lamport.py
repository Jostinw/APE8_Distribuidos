import socket
import threading
import time
import random

# ── CONFIGURAR EN CADA PC ──────────────────────
MY_ID = 0           # 0=PC1, 1=PC2, 2=PC3, 3=PC4
MY_IP = '192.168.1.10'  # IP de esta PC
PORT = 6000
# ──────────────────────────────────────────────

PEERS = {
    0: '192.168.1.10',
    1: '192.168.1.11',
    2: '192.168.1.12',
    3: '192.168.1.13',
}

lamport_clock = 0
lock = threading.Lock()
log = []

def increment_and_get():
    global lamport_clock
    with lock:
        lamport_clock += 1
        return lamport_clock

def update_clock(received):
    global lamport_clock
    with lock:
        lamport_clock = max(lamport_clock, received) + 1
        return lamport_clock

def send_message(dest_id, text):
    clock = increment_and_get()
    msg = f"{MY_ID}|{clock}|{text}"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((PEERS[dest_id], PORT))
        s.sendall(msg.encode())
        s.close()
        entry = f"[SEND] PC{MY_ID}→PC{dest_id} | L={clock} | msg='{text}'"
        log.append(entry)
        print(entry)
    except Exception as e:
        print(f"[ERROR] No se pudo enviar a PC{dest_id}: {e}")

def handle_client(conn):
    data = conn.recv(1024).decode()
    conn.close()
    parts = data.split('|')
    src_id, recv_clock, text = int(parts[0]), int(parts[1]), parts[2]
    new_clock = update_clock(recv_clock)
    entry = f"[RECV] PC{src_id}→PC{MY_ID} | L_recibido={recv_clock} | L_nuevo={new_clock} | msg='{text}'"
    log.append(entry)
    print(entry)

def server_thread():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((MY_IP, PORT))
    server.listen(10)
    while True:
        conn, _ = server.accept()
        threading.Thread(target=handle_client, args=(conn,)).start()

# Iniciar servidor en hilo
threading.Thread(target=server_thread, daemon=True).start()
print(f"[PC{MY_ID}] Lamport server iniciado. Esperando 3 segundos...")
time.sleep(3)

# Enviar 3 mensajes a destinos distintos
mensajes = [
    "Hola desde PC" + str(MY_ID),
    "Evento " + str(random.randint(1,100)),
    "Mensaje final de PC" + str(MY_ID)
]

destinos = [i for i in PEERS if i != MY_ID]
for i, dest in enumerate(destinos[:3]):
    time.sleep(random.uniform(0.5, 1.5))
    send_message(dest, mensajes[i % len(mensajes)])

time.sleep(3)
print(f"\n=== LOG FINAL PC{MY_ID} ===")
for entry in log:
    print(entry)
