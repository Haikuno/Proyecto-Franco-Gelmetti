import pandas as pd

df_productos = pd.read_excel('productos.xlsx') # Guardar en DataFrame el input de productos
df_productos = df_productos.sort_values(["Demanda"], ascending=False) # Sortear por demanda

df_lista = pd.read_excel('lista.xlsx') # Lista de ubicaciones

ids_conocidos = []
modulos = []
productos = []
ubicaciones = []
output = []

class producto():
    def __init__(self, nombre, demanda, automatizable, canales, categoria):
        self.nombre = nombre
        self.demanda = demanda
        self.automatizable = automatizable
        self.canales = canales
        self.categoria = categoria

class modulo():
    def __init__(self, id, ubicacion):
        self.ubicaciones_modulo = [ubicacion]
        self.categoria = "None"
        self.id = id

#--------------------------------------------------------------------------------#

for row in df_productos.itertuples():
    productos.append(producto(row[1], row[2], row[3], row[4], row[5]))

for row in df_lista.itertuples():
    ubi = str(row[1])
    if len(ubi) == 6:
            ubi = "0" + ubi
    ubicaciones.append(ubi)
    if row[0] > 900: # Ubicación actual
        id = ubi[:5]

        if id not in ids_conocidos:
            modulos.append(modulo(id, ubi))
            ids_conocidos.append(id)

        else:
            for m in modulos:
                if m.id == id:
                    m.ubicaciones_modulo.append(ubi)
                    break;

#--------------------------------------------------------------------------------#

currentub = 0 # Ubicaciones actualmente ocupadas
lleno = False


while not lleno:

    lleno = True

    for prod in productos:

        if prod.automatizable and currentub<=900: # Si es automatizable y no estan ocupadas todas las ubicaciones automaticas
            for i in range(prod.canales):
                output.append(
                    {'Nombre': prod.nombre,
                    'Ubicación': ubicaciones[currentub],
                    'Demanda': prod.demanda,
                    'Categoria': prod.categoria})
                currentub +=1
                productos.remove(prod)

        else:
            for i in range(prod.canales):
                for m in modulos:
                    if ubicaciones[currentub] in m.ubicaciones_modulo:
                        if m.categoria == "None" or m.categoria == prod.categoria:
                            m.categoria = prod.categoria
                            output.append(
                            {'Nombre': prod.nombre,
                            'Ubicación': ubicaciones[currentub],
                            'Demanda': prod.demanda,
                            'Categoria': prod.categoria})
                            currentub +=1
                            productos.remove(prod)
                            lleno = False
                            break
                        # elif ubicaciones[currentub] not in output:
                        #     output.append(
                        #     {'Nombre': " ",
                        #     'Ubicación': ubicaciones[currentub],
                        #     'Demanda': " ",
                        #     'Categoria': " "})
                        #     break

if lleno:
    output.append(
    {'Nombre': "Basura",
    'Ubicación': "Basura",
    'Demanda': "Basura",
    'Categoria': "Basura"})
    for prod in productos:
        output.append(
        {'Nombre': prod.nombre,
        'Ubicación': " ",
        'Demanda': prod.demanda,
        'Categoria': prod.categoria})



#--------------------------------------------------------------------------------#

output = pd.DataFrame(output)

#TODO:cambiar pathing dependiendo de pc

output.to_excel(r'/home/agu/Code/Proyecto-Franco-Gelmetti/Output.xlsx', index = False) # Archivo final