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

def printArtworksByMedium(sortMedium, cantObras):
    """
    Imprime la informacion del requerimiento n obras de
    """
    tableSortMedium = PrettyTable(["ObjectID", "Titulo", "Fecha", "Tecnica"])
    i = 1
    while i <= cantObras:
        artwork = lt.getElement(sortMedium, i)
        tableSortMedium.add_row([artwork["ObjectID"], artwork["Title"],
                                 artwork["Date"], artwork["Medium"]])
        i += 1
    tableSortMedium.max_width = 40
    tableSortMedium.hrules = ALL
    print("\n" + "-"*23 + " Req n. Answer " + "-"*24)
    print(tableSortMedium)


# Menu de opciones

def printMenu():
    print("\n" + "-"*20 + " Bienvenido al Reto 2 " + "-"*20)
    print("0 - Cargar información en el catálogo")
    print("1 - Las n obras mas antiguas para un medio especifico")
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
    inputs = input('Seleccione una opción para continuar: ')
    if int(inputs[0]) == 0:
        print("-"*61)
        print("Cargando información de los archivos ....")
        catalog = initCatalog()
        loadData(catalog)
        print("-"*61)

    elif int(inputs[0]) == 1:
        print("\n" + "-"*23 + " Req n. Inputs " + "-"*24)
        mediumName = input("Indique la tecnica que desea buscar: ")
        mediumMap = controller.getArworksbyMedium(catalog, mediumName)
        mediumArt = mediumMap["artworks"]
        sizeMedium = lt.size(mediumArt)
        sortMedium = controller.sortDateArtworks(mediumArt, sizeMedium)
        cantObras = input("Indique la cantidad de obras antiguas a imprimir "
                          "(menor o igual a " + str(sizeMedium) + "): ")
        printArtworksByMedium(sortMedium, int(cantObras))

    else:
        sys.exit(0)
sys.exit(0)
