#Cosas para correr el programa:
# Python
# Pandas datatable
# Openpyxl

# pip install openpyxl
# pip install pandas
import pandas as pd

df = pd.read_excel('gelme.xlsx') # Guardar en DataFrame el input
df = df.sort_values(["Demanda"], ascending=False) # Sortear por demanda

productos = []


class estacion():
    ubicacion = 0
    capacidad = 0
    cont = 0
    def __init__(self, ubicacion, capacidad, cont):
        self.ubicacion = ubicacion
        self.capacidad = capacidad
        self.cont = cont

class producto():
    nombre = ""
    demanda = 0
    automatizable = False
    canales = 0
    def __init__(self, nombre, demanda, automatizable, canales):
        self.nombre = nombre
        self.demanda = demanda
        self.automatizable = automatizable
        self.canales = canales

estacion0 = estacion(3100000, 108, 0)
estacion1 = estacion(3200000, 108, 0)
estacion2 = estacion(3300000, 108, 0)
estacion3 = estacion(3400000, 108, 0)
estacion4 = estacion(2100000, 108, 0)
estacion5 = estacion(2200000, 108, 0)
estacion6 = estacion(2300000, 108, 0)
estacion7 = estacion(1100000, 144, 0)

estaciones = [estacion0, estacion1, estacion2, estacion3, estacion4, estacion5, estacion6, estacion7]

for row in df.itertuples():
    productos.append(producto(row[1], row[2], row[3], row[4])) #


output = []

maxub=0 # Máximo de ubicaciones

estacionlibre = estacion0

for prod in productos:
    if prod.automatizable and maxub<900:
        for i in range(prod.canales):
            estacionlibre.cont += 1
            output.append({'Nombre': prod.nombre, 'Ubicación': estacionlibre.ubicacion, 'Demanda': prod.demanda})
            estacionlibre.ubicacion += 1
            maxub +=1
        for estacion in estaciones:
            if estacion.cont < estacionlibre.cont and estacion.cont + prod.canales < estacion.capacidad:
                estacionlibre = estacion

output = pd.DataFrame(output)

#TODO:cambiar pathing dependiendo de pc
output.to_excel(r'/home/agu/code/proyecto/Output.xlsx', index = False) # Archivo final

#8 estaciones
# 7 de 108 ubicaciones
# 1 de 144 ubicaciones
# 900 ubicaciones