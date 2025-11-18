import multiprocessing
import random


def productor(cola):
    ips_posibles = ["192.168.1.10", "10.0.0.5", "172.16.0.1", "192.168.1.10"]
    for _ in range(20):
        ip = random.choice(ips_posibles)
        cola.put(ip)
    cola.put('FIN')

def consumidor(cola):
    generadas = {}
    while True:
        ip = cola.get()
        if ip == 'FIN':
            break

        generadas[ip] = generadas.get(ip, 0) + 1

    print(f"Resumen de tráfico: {generadas}")

    print("--- ESCRIBIENDO ARCHIVO ---")

    nombre_archivo = "sospechosos.txt"
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write("--- IPs SOSPECHOSAS (>3 intentos) ---\n")
        for ip, cantidad in generadas.items():
            if cantidad > 3:
                archivo.write(f"{ip} - Intentos: {cantidad}\n")

    print("Archivo sospechosos.txt generado.")

if __name__ == "__main__":

    q = multiprocessing.Queue()
    p1 = multiprocessing.Process(target=consumidor, args=(q,))
    p2 = multiprocessing.Process(target=productor, args=(q,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()
