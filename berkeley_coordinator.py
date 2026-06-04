import socket
import time
import threading

COORDINATOR_IP = '192.168.1.10'
PORT = 5001
SLAVES = ['192.168.1.11', '192.168.1.12', '192.168.1.13']

slave_times = {}
lock = threading.Lock()

def get_slave_time(ip):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, PORT))
        data = s.recv(1024)
        t_slave = float(data.decode())
        s.close()
        with lock:
            slave_times[ip] = t_slave
        print(f"[COORD] Hora de {ip}: {time.strftime('%H:%M:%S', time.localtime(t_slave))}")
    except Exception as e:
        print(f"[ERROR] No se pudo conectar a {ip}: {e}")

def send_adjustment(ip, offset):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, PORT + 1))
        s.sendall(str(offset).encode())
        s.close()
        print(f"[COORD] Ajuste enviado a {ip}: {offset:+.3f} segundos")
    except Exception as e:
        print(f"[ERROR] No se pudo enviar ajuste a {ip}: {e}")

print("=== ALGORITMO DE BERKELEY - COORDINADOR ===")
print(f"Mi hora local: {time.strftime('%H:%M:%S')}")

# Esperar que los esclavos estén listos
input("Presiona ENTER cuando todos los esclavos estén corriendo...")

# Paso 1: Pedir hora a todos los esclavos
threads = [threading.Thread(target=get_slave_time, args=(ip,)) for ip in SLAVES]
for t in threads: t.start()
for t in threads: t.join()

# Paso 2: Calcular promedio (incluyendo mi propio tiempo)
my_time = time.time()
all_times = list(slave_times.values()) + [my_time]
average = sum(all_times) / len(all_times)

print(f"\nPromedio calculado: {time.strftime('%H:%M:%S', time.localtime(average))}")

# Paso 3: Calcular y enviar offsets
my_offset = average - my_time
print(f"Mi propio ajuste: {my_offset:+.3f} segundos")

adj_threads = []
for ip in slave_times:
    offset = average - slave_times[ip]
    t = threading.Thread(target=send_adjustment, args=(ip, offset))
    adj_threads.append(t)
for t in adj_threads: t.start()
for t in adj_threads: t.join()

print("\n[COORD] Sincronización Berkeley completada.")
