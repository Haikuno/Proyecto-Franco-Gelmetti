import pandas as pd
import os


class Producto():
    def __init__(self, nombre, categoria, automatizable):
        self.nombre = nombre
        self.categoria = categoria
        self.automatizable = automatizable
    ubicacion = None


class Ubicacion():
    def __init__(self, id, modulo, automatizable):
        self.id = id
        self.modulo = modulo
        self.automatizable = automatizable


class Modulo():
    def __init__(self, id):
        self.id = id
    categoria = None


def computar(archivo):

    if archivo is None:
        return

    directorio = os.getcwd()

    # Guardar en DataFrame el input de productos
    df_productos = pd.read_excel(archivo)
    df_productos = df_productos.sort_values(
        ["Demanda"], ascending=False)  # Sortear por demanda por las dudas

    # Lista de ubicaciones
    df_lista = pd.read_excel(directorio + r'/listaprio.xlsx')
    df_lista = df_lista.sort_values(["Prioridad"], ascending=True)

    productos = []
    ubicaciones = []
    modulos = []
    modulos_ocupados = []  # ID
    output = []

    for row in df_productos.itertuples():
        productos.append(
            Producto(row.Nombre, row.Categoría, row.Automatizable))

    for row in df_lista.itertuples():
        if str(row.Ubicación).startswith('A'):  # Automatizable
            ubicaciones.append(Ubicacion(row.Ubicación, row.Módulo, True))
        else:
            ubicaciones.append(Ubicacion(row.Ubicación, row.Módulo, False))

        modulo = Modulo(row.Módulo)
        if len(modulos) == 0:
            modulos.append(modulo)

        if modulo.id not in modulos_ocupados:
            modulos.append(modulo)
            modulos_ocupados.append(modulo.id)

    for producto in productos:

        for ubicacion in ubicaciones:
            if producto.ubicacion is not None:
                break
            for modulo in modulos:
                if ubicacion.modulo == modulo.id:
                    if producto.automatizable == False:
                        if ubicacion.automatizable == True:
                            continue
                    if modulo.categoria is None or modulo.categoria == producto.categoria:
                        modulo.categoria = producto.categoria
                        producto.ubicacion = ubicacion.id
                        del(ubicaciones[ubicaciones.index(ubicacion)])
                        break

    for producto in productos:
        output.append({
            'Nombre': producto.nombre,
            'Ubicación': producto.ubicacion,
            'Categoria': producto.categoria,
            'Automatizable': producto.automatizable,
        })

    #--------------------------------------------------------------------------------#

    output = pd.DataFrame(output)

    output.to_excel(directorio + r'/Output.xlsx', index=False)  # Archivo final
