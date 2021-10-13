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
from DISClib.ADT import map as mp
assert cf

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

default_limit = 1000
sys.setrecursionlimit(default_limit*10)


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


def printArtistBeginDate(rangeArtists, anio1, anio2, total):
    """
    Imprime los datos requeridos para el requerimiento 1
    """
    tbArtists = PrettyTable(["Nombre", "Año de nacimiento", "Año de "
                             "fallecimiento", "Nacionalidad", "Genero"])
    mapDate = catalog["dates"]
    pos = 1
    u = 1
    while u < 4:
        key = lt.getElement(rangeArtists, pos)
        artists = mp.get(mapDate, key)
        for artist in lt.iterator(artists["value"]["artists"]):
            if u == 4:
                break
            tbArtists.add_row([artist["DisplayName"], artist["BeginDate"],
                               artist["EndDate"], artist["Nationality"],
                               artist["Gender"]])
            u += 1
        pos += 1
    listaUltimos = lt.newList("SINGLE_LINKED")
    pos2 = lt.size(rangeArtists)
    i = 1
    while i < 4:
        key = lt.getElement(rangeArtists, pos2)
        artists = mp.get(mapDate, key)
        for artist in lt.iterator(artists["value"]["artists"]):
            if i == 4:
                break
            lt.addFirst(listaUltimos, artist)
            i += 1
        pos2 -= 1
    for artist in lt.iterator(listaUltimos):
        tbArtists.add_row([artist["DisplayName"], artist["BeginDate"],
                           artist["EndDate"], artist["Nationality"],
                           artist["Gender"]])
    tbArtists.max_width = 40
    tbArtists.hrules = ALL
    print("\n" + "-"*23 + " Req 1. Answer " + "-"*24)
    print("Hay " + str(total) + " artistas que nacieron entre " + anio1 + " y "
          + anio2)
    print("\n" + "Los tres primeros y tres ultimos artistas son:")
    print(tbArtists)


def printArtworkDateAcquired(sortArtRange, fecha1, fecha2, compras, total):
    """
    Imprime los datos requeridos para el requerimiento 2
    """
    tbArtworks = PrettyTable(["Titulo", "Artista(s)", "Fecha", "Medio",
                              "Dimensiones"])
    mapDate = catalog["artDateAcquired"]
    pos = 1
    u = 1
    while u < 4:
        key = lt.getElement(sortArtRange, pos)
        artworks = mp.get(mapDate, key)
        for artwork in lt.iterator(artworks["value"]["artworks"]):
            if u == 4:
                break
            tbArtworks.add_row([artwork["Title"], artwork["NombresArtistas"],
                                artwork["DateAcquired"], artwork["Medium"],
                                artwork["Dimensions"]])
            u += 1
        pos += 1
    listaUltimos = lt.newList("SINGLE_LINKED")
    pos2 = lt.size(sortArtRange)
    i = 1
    while i < 4:
        key = lt.getElement(sortArtRange, pos2)
        artworks = mp.get(mapDate, key)
        for artwork in lt.iterator(artworks["value"]["artworks"]):
            if i == 4:
                break
            lt.addFirst(listaUltimos, artwork)
            i += 1
        pos2 -= 1
    for artwork in lt.iterator(listaUltimos):
        tbArtworks.add_row([artwork["Title"], artwork["NombresArtistas"],
                            artwork["DateAcquired"], artwork["Medium"],
                            artwork["Dimensions"]])
    tbArtworks.max_width = 40
    tbArtworks.hrules = ALL
    print("\n" + "-"*23 + " Req 2. Answer " + "-"*24)
    print("El MoMA adquirió " + str(total) + " obras unicas entre " + fecha1
          + " y " + fecha2)
    print("El numero total de obras adquiridas por compra es: " + compras)
    print("\n" + "Las tras primeras y tres ultimas obras adquiridas son:")
    print(tbArtworks)


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

    print("9 - Contar las obras de una nacionalidad")
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
        print("\n" + "-"*23 + " Req 1. Inputs " + "-"*24)
        anio1 = str(input("Indique el año inicial con la que desea "
                          "iniciar el rango: "))
        anio2 = str(input("Indique el año final con la que desea finalizar "
                          "el rango: "))
        start_time = time.process_time()
        tpArt = controller.getAuthorsByDate(catalog, anio1, anio2)
        total = tpArt[1]
        rangeArtists = controller.sortArtists(tpArt[0], lt.size(tpArt[0]))
        stop_time = time.process_time()
        elapsed_time_mseg = round((stop_time - start_time)*1000, 2)
        print("Tiempo:", elapsed_time_mseg, "mseg")
        printArtistBeginDate(rangeArtists, anio1, anio2, total)

    elif int(inputs[0]) == 2:
        print("\n" + "-"*23 + " Req 2. Inputs " + "-"*24)
        fecha1 = str(input("Indique la fecha inicial con la que desea "
                           "iniciar el rango (YYYY-MM-DD): "))
        fecha2 = str(input("Indique la fecha final con la que desea finalizar "
                           "el rango (YYYY-MM-DD): "))
        start_time = time.process_time()
        tupleArtRange = controller.artworksRange(catalog, fecha1, fecha2)
        ltArtRange = tupleArtRange[0]
        compras = str(tupleArtRange[1])
        total = tupleArtRange[2]
        sortArtRange = controller.sortArtWorks(ltArtRange, lt.size(ltArtRange))
        stop_time = time.process_time()
        elapsed_time_mseg = round((stop_time - start_time)*1000, 2)
        print("Tiempo:", elapsed_time_mseg, "mseg")
        printArtworkDateAcquired(sortArtRange, fecha1, fecha2, compras, total)

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

    elif int(inputs[0]) == 9:
        print("\n" + "-"*23 + " Req n. Inputs " + "-"*24)
        nationalityName = input("Indique la nacionalidad que desea buscar: ")
        start_time = time.process_time()
        natDict = controller.getArworksbyNationality(catalog, nationalityName)
        cantidad = lt.size(natDict["artworks"])
        stop_time = time.process_time()
        elapsed_time_mseg = round((stop_time - start_time)*1000, 2)
        print("Tiempo:", elapsed_time_mseg, "mseg")
        print("\n" + "-"*23 + " Req n. Answer " + "-"*24)
        print("Hay " + str(cantidad) + " obras para la nacionalidad "
              + nationalityName)

    else:
        sys.exit(0)
sys.exit(0)
