import socket
import time

HOST = '192.168.1.10'
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(10)

print("=" * 50)
print("   ALGORITMO DE CRISTIAN - SERVIDOR (PC1)")
print("=" * 50)
print(f"Servidor escuchando en {HOST}:{PORT}")
print(f"Mi hora actual: {time.strftime('%H:%M:%S')}")
print("-" * 50)
print("Esperando clientes...\n")

contador = 0
while True:
    conn, addr = server.accept()
    t2 = time.time()
    timestamp = str(t2).encode()
    conn.sendall(timestamp)
    conn.close()
    contador += 1
    print(f"[Cliente #{contador}] Respondí a {addr[0]}")
    print(f"   Hora enviada (t2): {time.strftime('%H:%M:%S', time.localtime(t2))}.{int((t2%1)*1000):03d}")
    print()
