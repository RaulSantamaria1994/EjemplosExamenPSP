import multiprocessing
import time


def vendedor(id_vendedor, candado):
    ventas_propias = 0
    for _ in range(3):  # Intenta vender 3 veces

        with candado:  # 🔒 INICIO ZONA CRÍTICA
            # Modo 'r+' permite leer y escribir sin borrar el archivo al abrirlo
            with open("stock.txt", "r+") as f:
                contenido = f.read()
                stock_actual = int(contenido)

                if stock_actual > 0:
                    # Simulamos lentitud para provocar error si no hubiera Lock
                    time.sleep(0.1)

                    stock_actual -= 1

                    # Rebobinamos al principio para sobrescribir
                    f.seek(0)
                    f.write(str(stock_actual))

                    # IMPORTANTE: Truncar por si el numero nuevo tiene menos dígitos
                    # (ej: pasar de 10 a 9, para no dejar 90)
                    f.truncate()

                    print(f"✅ Vendedor {id_vendedor}: Vendió una. Quedan {stock_actual}")
                    ventas_propias += 1
                else:
                    print(f"❌ Vendedor {id_vendedor}: Stock Agotado.")
                    break  # Salimos del bucle for
        # 🔓 FIN ZONA CRÍTICA


if __name__ == "__main__":
    # Inicializar stock
    with open("stock.txt", "w") as f:
        f.write("10")

    candado = multiprocessing.Lock()
    procesos = []

    for i in range(5):
        p = multiprocessing.Process(target=vendedor, args=(i + 1, candado))
        procesos.append(p)
        p.start()

    for p in procesos:
        p.join()

    print("--- FIN DE VENTAS ---")