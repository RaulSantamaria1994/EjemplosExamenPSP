import multiprocessing

cuentas = {"admin": "1234", "juan": "secreto", "ana": "python"}

def cliente(conexion, usuario, contras):
    datos = (usuario, contras)
    conexion.send(datos)

    acceso = conexion.recv()

    if acceso:
        print("ACCESO CONCEDIDO")

    else:
        print("ACCESO DENEGADO")


def servidor(conexion):
    datos = conexion.recv()
    acceso = False
    for k, v in cuentas.items():
        if v == datos[1] and k == datos[0]:
            acceso = True
            break

    conexion.send(acceso)

if __name__ == '__main__':
    usuario = input("Introduce un usuario: ")
    contras = input("Introduce un contraseña: ")

    cliente_servidor, servidor_cliente = multiprocessing.Pipe()

    p1 = multiprocessing.Process(target=cliente, args=(servidor_cliente, usuario, contras))
    p2 = multiprocessing.Process(target=servidor, args=(cliente_servidor,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print("FIN")
