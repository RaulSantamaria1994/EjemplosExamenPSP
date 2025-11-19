import multiprocessing


def diccionario(conexion):

    palabra_recibida = conexion.recv()

    traduccion = ""
    palabras = {"hello": "hola", "cat": "gato", "dog": "perro", "code": "codigo"}

    for k, v in palabras.items():
        if k == palabra_recibida:
            traduccion = v
            break
        else:
            traduccion = "No encontrado"
    conexion.send(traduccion)

if __name__ == '__main__':
    palabra = input("Ingresa una palabra: ")

    main_diccionario, diccionario_main = multiprocessing.Pipe()

    p1 = multiprocessing.Process(target=diccionario, args=(diccionario_main,))
    p1.start()

    main_diccionario.send(palabra)

    p1.join()

    resultado = main_diccionario.recv()

    print("Traduccion:", resultado)