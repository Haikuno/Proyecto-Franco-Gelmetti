import pandas as pd
import os
import copy
from listaprio import *


# --------------------------------------   Clases   ------------------------------------------- #

class Producto():
    def __init__(self, nombre, categoria, automatizable, demanda):
        self.nombre = nombre
        self.categoria = categoria
        self.automatizable = automatizable
        self.demanda = demanda
        self.ubicacion = None


class Ubicacion():
    def __init__(self, id, modulo, automatizable):
        self.id = id
        self.modulo = modulo
        self.automatizable = automatizable


class Modulo():
    def __init__(self, id, automatizable):
        self.id = id
        self.categoria = None
        self.tamaño = 1
        self.automatizable = automatizable

class Categoria():
    def __init__(self, nombre):
        self.nombre = nombre
        self.productos = []
        self.demandas = []
        self.demandas_output = []

# -----------------------------------   Computar   ---------------------------------------- #

def computar(archivo):

    if archivo is None: # Si no se ha seleccionado ningún archivo
        return

    directorio = os.getcwd() # Obtener el directorio actual

    # Guardar en DataFrame el input de productos
    df_productos = pd.read_excel(archivo)
    df_productos = df_productos.sort_values(
        ["Demanda"], ascending=False)  # Sortear por demanda por las dudas

    productos = [] # Lista de productos
    ubicaciones = [] # Lista de ubicaciones
    auto = 0 # cantidad de ubicaciones automatizables
    modulos = dict() # Diccionario de modulos
    output = [] # Resultado
    categorias = dict() # Diccionario de categorías
    categorias["Automatizable"] = Categoria("Automatizable")



    # Llena la lista de productos con objetos producto
    for row in df_productos.itertuples():
        productos.append(
            Producto(row.Nombre, row.Categoría, row.Automatizable, row.Demanda))

    # Llena la lista ubicación y la lista módulos con sus objetos respectivos
    for ubicacion in listaprio:
        if str(ubicacion["Ubicación"]).startswith('A'):  # Automatizable
            ubicaciones.append(Ubicacion(ubicacion["Ubicación"], ubicacion["Módulo"], True))
            modulo = Modulo(ubicacion["Módulo"], automatizable=True)
            modulo.categoria = categorias["Automatizable"]
            auto += 1
        else:
            ubicaciones.append(Ubicacion(ubicacion["Ubicación"], ubicacion["Módulo"], False))
            modulo = Modulo(ubicacion["Módulo"], automatizable=False)


        if modulo.id not in modulos:
            modulos[modulo.id] = modulo

        else:
            modulos[modulo.id].tamaño += 1

    # Llena el diccionario de categorías con sus productos y demandas respectivas

    for producto in productos:

        if producto.automatizable and len(categorias["Automatizable"].productos) < auto:
            categorias["Automatizable"].productos.append(producto)
            categorias["Automatizable"].demandas.append(producto.demanda)
            categorias["Automatizable"].demandas_output.append(producto.demanda)
            continue


        if producto.categoria not in categorias.keys():
            categorias[producto.categoria] = Categoria(producto.categoria)

        categorias[producto.categoria].productos.append(producto)
        categorias[producto.categoria].demandas.append(producto.demanda)
        categorias[producto.categoria].demandas_output.append(producto.demanda)

    # Designa categoria de módulo según su demanda
    for modulo in modulos.values():

        if modulo.categoria != None:
            continue

        categoria = None

        # Busca la categoría con la demanda más alta
        for c in categorias.values():
            if categoria == None or sum(categoria.demandas) < sum(c.demandas):
                categoria = c

        modulo.categoria = categoria
        while modulo.tamaño != 0 and len(categoria.demandas) != 0:
            categoria.demandas.pop(0)
            modulo.tamaño -= 1

    # Designa productos a cada ubicación según la categoría del módulo respectivo y arma el output
    for ubicacion in ubicaciones:
        categoria = modulos[ubicacion.modulo].categoria

        if modulos[ubicacion.modulo].categoria == None:
            continue

        if len(categoria.productos) == 0:
            continue

        producto = copy.deepcopy(categoria.productos[0])
        categoria.productos.remove(categoria.productos[0])

        if producto == None:
            continue

        output.append({
            'Ubicación': ubicacion.id,
            'Nombre': producto.nombre,
            'Demanda': categoria.demandas_output.pop(0),
            'Categoría': producto.categoria,
            'Automatizable': producto.automatizable,
        })

    #--------------------------------------------------------------------------------#

    output = pd.DataFrame(output)

    output.sort_values('Demanda', ascending=False)

    output.to_excel(directorio + r'/Output.xlsx', index=False)  # Archivo final
