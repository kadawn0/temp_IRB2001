import os
from os import listdir


def get():
    lista = list()
    lista_alt = list()
    dir = os.path.dirname(__file__)
    for file in listdir(dir):
        if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg")\
                or file.endswith(".gif"):
            lista.append(os.path.join(dir, str(file))) # Solamente guarda los paths absolutos
            # dentro de esta carpeta si el archivo es una imagen en
            # los formatos especificados.
            lista_alt.append(str(file))

    return (dir, lista)

all = get()