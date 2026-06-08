import socket
import time

MY_PC = "PC2"           # ← CAMBIAR: "PC2", "PC3" o "PC4"
SERVER_IP = '192.168.1.10'
PORT = 5000

print("=" * 50)
print(f"   ALGORITMO DE CRISTIAN - CLIENTE ({MY_PC})")
print("=" * 50)
print(f"Mi hora LOCAL antes del ajuste: {time.strftime('%H:%M:%S')}")
print(f"(Esta hora está desincronizada a propósito)")
print("-" * 50)

input("\nPresiona ENTER para solicitar hora al servidor...")

# ── t1: momento antes de enviar ──────────────
t1 = time.time()
print(f"\nt1 (antes de enviar):    {time.strftime('%H:%M:%S', time.localtime(t1))}.{int((t1%1)*1000):03d}")

# ── Enviar solicitud al servidor ─────────────
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, PORT))
data = client.recv(1024)
client.close()

# ── t3: momento al recibir respuesta ─────────
t3 = time.time()
t2 = float(data.decode())

print(f"t2 (hora del servidor):  {time.strftime('%H:%M:%S', time.localtime(t2))}.{int((t2%1)*1000):03d}")
print(f"t3 (al recibir):         {time.strftime('%H:%M:%S', time.localtime(t3))}.{int((t3%1)*1000):03d}")

# ── Cálculos ──────────────────────────────────
RTT    = t3 - t1
Delay  = RTT / 2
Nuevo_Tiempo = t2 + Delay
diferencia = Nuevo_Tiempo - t3  # diferencia con hora "real" de red

print("\n" + "=" * 50)
print("   RESULTADOS")
print("=" * 50)
print(f"RTT (t3 - t1):           {RTT*1000:.3f} ms")
print(f"Delay (RTT / 2):         {Delay*1000:.3f} ms")
print(f"Tiempo ajustado:         {time.strftime('%H:%M:%S', time.localtime(Nuevo_Tiempo))}.{int((Nuevo_Tiempo%1)*1000):03d}")
print(f"Diferencia con servidor: {diferencia*1000:+.3f} ms")
print("=" * 50)

if abs(diferencia) < 0.1:
    print("✓ Reloj sincronizado correctamente (error < 100ms)")
else:
    print(f"⚠ Diferencia notable: {diferencia:.4f} segundos")