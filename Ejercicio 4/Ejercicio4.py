import multiprocessing
import random

archivo = "urnas.txt"

def mesas(id_mesa, candado):
    partidos_posibles = ["Partido A", "Partido B", "Partido C"]
    for i in range(10):
        votos = random.choice(partidos_posibles)

        with candado:
            with open(archivo, "a", encoding="utf-8") as arch:
                linea = f"Mesa: {id_mesa}: VOTO por {votos}\n"
                arch.write(linea)

        print(f"Caja {id_mesa} registró el voto {i + 1}")

if __name__ == '__main__':
    # Limpiar archivo previo
    with open("urnas.txt", "w", encoding="utf-8") as f:
        f.write("INICIO DE RECUENTO\n")

    candado = multiprocessing.Lock()
    procesos = []

    for i in range(4):
        p = multiprocessing.Process(target=mesas, args=(i + 1, candado))
        procesos.append(p)
        p.start()

    for p in procesos:
        p.join()

    conteo = {}

    with open("urnas.txt", "r") as f:
        for line in f:
            voto = line.strip()
            if voto:
                conteo[voto] = conteo.get(voto, 0) + 1

    print("Recuento:", conteo)

    ganador = max(conteo, key=conteo.get)
    print(f"\nEl ganador es: {ganador} con {conteo[ganador]} votos\n")
