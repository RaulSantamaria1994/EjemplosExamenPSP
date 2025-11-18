import multiprocessing
import time
import random


def caja_registradora(id_caja, candado):
    for i in range(5):
        venta = {"producto": f"Item-{random.randint(1, 100)}", "precio": random.randint(5, 50)}
        time.sleep(random.uniform(0.1, 0.5))

        # ZONA CRÍTICA: Solo una caja escribe a la vez
        with candado:
            with open("ventas_dia.txt", "a", encoding="utf-8") as f:
                linea = f"Caja {id_caja}: Vendido {venta['producto']} por ${venta['precio']}\n"
                f.write(linea)
        print(f"Caja {id_caja} registró venta {i + 1}")


if __name__ == "__main__":
    # Limpiar archivo previo
    with open("ventas_dia.txt", "w") as f:
        f.write("INICIO DE VENTAS\n")

    candado = multiprocessing.Lock()
    procesos = []

    for i in range(3):
        p = multiprocessing.Process(target=caja_registradora, args=(i + 1, candado))
        procesos.append(p)
        p.start()

    for p in procesos:
        p.join()

    print("Todas las cajas han cerrado. Revisa ventas_dia.txt")