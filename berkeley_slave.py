import socket
import time

MY_IP = '192.168.1.11'  # ← CAMBIAR según cada PC (11, 12, 13)
PORT = 5001

print("=== ALGORITMO DE BERKELEY - ESCLAVO ===")
print(f"Mi hora local: {time.strftime('%H:%M:%S')}")

# Servidor para responder con mi hora
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((MY_IP, PORT))
server.listen(1)
print("Esperando solicitud del coordinador...")

conn, addr = server.accept()
my_time = time.time()
conn.sendall(str(my_time).encode())
conn.close()
server.close()
print(f"Envié mi hora: {time.strftime('%H:%M:%S', time.localtime(my_time))}")

# Esperar el ajuste del coordinador
server2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server2.bind((MY_IP, PORT + 1))
server2.listen(1)
print("Esperando ajuste del coordinador...")

conn2, _ = server2.accept()
offset = float(conn2.recv(1024).decode())
conn2.close()
server2.close()

nuevo_tiempo = time.time() + offset
print(f"Ajuste recibido: {offset:+.3f} segundos")
print(f"Nueva hora ajustada: {time.strftime('%H:%M:%S', time.localtime(nuevo_tiempo))}")