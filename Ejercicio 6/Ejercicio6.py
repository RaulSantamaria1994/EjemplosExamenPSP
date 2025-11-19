import multiprocessing
import random
import time


def generador(cola1):
    archivos = ["foto.jpg", "documento.pdf", "imagen.png", "texto.txt"]
    for _ in range(20):
        generado = random.choice(archivos)
        cola1.put(generado)
        print("GENERADO:", generado)
        time.sleep(0.3)

    # Señal de fin
    cola1.put(None)
    print("FIN DEL GENERADOR")


def filtro(cola1, cola2):
    filtrado = []

    while True:
        recibido = cola1.get()

        if recibido is None:   # fin del generador
            break

        if ".jpg" in recibido or ".png" in recibido:
            filtrado.append(recibido)
            print("FILTRADO:", recibido)

    cola2.put(filtrado)
    cola2.put(None)
    print("FIN DEL FILTRO")


def archivador(cola2):
    while True:
        recibido = cola2.get()
        if recibido is None:
            break

        archivado = {}
        for elemento in recibido:
            archivado[elemento] = "Guardado"

        print("ARCHIVADO:", archivado)

    print("FIN DEL ARCHIVADOR")


if __name__ == '__main__':
    cola1 = multiprocessing.Queue()
    cola2 = multiprocessing.Queue()

    p1 = multiprocessing.Process(target=generador, args=(cola1,))
    p2 = multiprocessing.Process(target=filtro, args=(cola1, cola2))
    p3 = multiprocessing.Process(target=archivador, args=(cola2,))

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()
