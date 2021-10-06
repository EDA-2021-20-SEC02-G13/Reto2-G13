"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

from prettytable import PrettyTable, ALL
import config as cf
import time
import sys
import controller
from DISClib.ADT import list as lt
assert cf

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


# Funciones para la impresión de resultados

def printCargaArchivos(catalog, sizeArtists, sizeArtworks):
    """
    Imprime los datos requeridos para la carga de archivos
    """
    print("-"*62)
    print("Artistas cargados: " + str(sizeArtists))
    print("Obras cargadas: " + str(sizeArtworks))
    print("-"*62)
    for pos in range(sizeArtists-2, sizeArtists+1):
        print(lt.getElement(catalog["artists"], pos))
    for pos2 in range(sizeArtworks-2, sizeArtworks+1):
        print(lt.getElement(catalog["artworks"], pos2))
    print("-"*62)


def printArtistArtworks(obras, nombre, constituentID, tecnicas):
    """
    Imprime los datos requeridos para el requerimiento 3
    """
    tableObras = PrettyTable(["Titulo", "Fecha", "Medio", "Dimensiones"])
    size = lt.size(obras)
    for pos in range(1, 4):
        obra = lt.getElement(obras, pos)
        tableObras.add_row([obra["Title"], obra["Date"], obra["Medium"],
                            obra["Dimensions"]])
    if size == 4:
        obra = lt.getElement(obras, size)
        tableObras.add_row([obra["Title"], obra["Date"], obra["Medium"],
                            obra["Dimensions"]])
    elif size == 5:
        for pos in range(size-1, size+1):
            obra = lt.getElement(obras, pos)
            tableObras.add_row([obra["Title"], obra["Date"], obra["Medium"],
                                obra["Dimensions"]])
    elif size > 5:
        for pos in range(size-2, size+1):
            obra = lt.getElement(obras, pos)
            tableObras.add_row([obra["Title"], obra["Date"], obra["Medium"],
                                obra["Dimensions"]])
    tableObras.max_width = 40
    tableObras.hrules = ALL
    print("\n" + "-"*23 + " Req 3. Answer " + "-"*24)
    print(nombre + " con ID " + constituentID + ", tiene " +
          str(tecnicas[2]) + " piezas artisticas en el MoMA.")
    print("El/la artista utilizó " + str(tecnicas[1]) + " técnicas distintas.")
    print("\n" + "La técnica que más se utilizó fue " + tecnicas[0] +
          ". A continuación se muestra el listado de obras con dicha técnica.")
    print(tableObras)


# Menu de opciones

def printMenu():
    print("\n" + "-"*20 + " Bienvenido al Reto 2 " + "-"*20)
    print("0 - Cargar información en el catálogo")
    print("1 - Req 1. Listar cronológicamente a los artistas")
    print("2 - Req 2. Listar cronológicamente a las adquisiciones")
    print("3 - Req 3. Clasificar las obras de un artista por técnica")
    print("4 - Req 4. Clasificar las obras por la nacionalidad de sus"
          " creadores")
    print("5 - Req 5. Transportar obras de un departamento")
    print("6 - Bono. Encontrar los artistas mas prolificos del museo")
    print("7 - Salir de la aplicación")
    print("-"*62)


# Funciones de inicializacion

def initCatalog():
    """
    Inicializa el catalogo del MoMA
    """
    return controller.initCatalog()


def loadData(catalog):
    """
    Carga la informacion del MoMA en el catalogo
    """
    controller.loadData(catalog)


# Menu principal

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input("Seleccione una opción para continuar: ")

    if int(inputs[0]) == 0:
        print("-"*61)
        print("Cargando información de los archivos ....")
        start_time = time.process_time()
        catalog = initCatalog()
        loadData(catalog)
        sizeArtists = lt.size(catalog["artists"])
        sizeArtworks = lt.size(catalog["artworks"])
        stop_time = time.process_time()
        elapsed_time_mseg = round((stop_time - start_time)*1000, 2)
        print("Tiempo:", elapsed_time_mseg, "mseg")
        printCargaArchivos(catalog, sizeArtists, sizeArtworks)

    elif int(inputs[0]) == 1:
        pass

    elif int(inputs[0]) == 2:
        pass

    elif int(inputs[0]) == 3:
        print("\n" + "-"*23 + " Req 3. Inputs " + "-"*24)
        nombre = str(input("Indique el nombre del artista: "))
        start_time = time.process_time()
        constituentID = controller.constituentID(nombre, catalog)
        mapTecnicas = controller.artistArtworks(constituentID, catalog)
        tecnicas = controller.artistMedium(mapTecnicas)
        obras = controller.getArworksbyMedium(catalog, tecnicas[0])
        stop_time = time.process_time()
        elapsed_time_mseg = round((stop_time - start_time)*1000, 2)
        print("Tiempo:", elapsed_time_mseg, "mseg")
        printArtistArtworks(obras["artworks"], nombre, constituentID, tecnicas)

    elif int(inputs[0]) == 4:
        pass

    elif int(inputs[0]) == 5:
        pass

    elif int(inputs[0]) == 6:
        pass

    else:
        sys.exit(0)
sys.exit(0)
