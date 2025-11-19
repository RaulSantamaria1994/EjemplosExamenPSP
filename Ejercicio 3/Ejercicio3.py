import multiprocessing
import random
import time


def camion(cola):
    carga = {
        "Cajas": random.randint(1, 100),
        "Palets": random.randint(1, 50)
    }
    time.sleep(1)
    cola.put(carga)


if __name__ == '__main__':
    q = multiprocessing.Queue()

    procesos = []

    for _ in range(3):
        p = multiprocessing.Process(target=camion, args=(q,))
        procesos.append(p)
        p.start()

    for p in procesos:
        p.join()

    cargas = [q.get() for _ in procesos]

    total = {"Cajas": 0, "Palets": 0}

    for carga in cargas:
        total["Cajas"] += carga["Cajas"]
        total["Palets"] += carga["Palets"]

    print("Total acumulado:", total)
