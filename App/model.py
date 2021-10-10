"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """

import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as ms
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos
listas, una para los videos, otra para las categorias de los mismos
"""


# Construccion de modelos

def newCatalog():
    """
    Inicializa el catalogo del MoMA
    """
    catalog = {"artists": None,
               "artworks": None,
               "mediums": None}

    catalog["artists"] = lt.newList("SINGLE_LINKED")

    catalog["artworks"] = lt.newList("SINGLE_LINKED")

    catalog["mediums"] = mp.newMap(250,
                                   maptype="PROBING",
                                   loadfactor=0.5,
                                   comparefunction=compareMedium)

    catalog["nationalities"] = mp.newMap(118,
                                         maptype="CHAINING",
                                         loadfactor=4,
                                         comparefunction=compareNationality)

    catalog["artDateAcquired"] = mp.newMap(32800,
                                           maptype="PROBING",
                                           loadfactor=0.5,
                                           comparefunction=compareDateAcquired)

    return catalog


# Funciones para agregar informacion al catalogo

def addArtist(catalog, artist):
    """
    Adiciona un artista a la lista de artistas, la cual guarda referencias
    a la informacion de dicho artista
    """
    lt.addLast(catalog["artists"], artist)


def addArtwork(catalog, artwork):
    """
    Adiciona una obra a lista de obras, la cual guarda referencias a la
    informacion de dicha obra
    """
    lt.addLast(catalog["artworks"], artwork)
    nacionalidades = nationalityArtistsinArtwork(artwork, catalog["artists"])
    for nacionalidad in lt.iterator(nacionalidades):
        addArtworkNationality(catalog, nacionalidad, artwork)


def addArtworkRange(catalog, fecha, artwork):
    """
    Adiciona una obra a la lista de fechas que contienen una fecha de
    adquisicion en especifico
    """
    fechas = catalog["artDateAcquired"]
    existfecha = mp.contains(fechas, fecha)
    if existfecha:
        entry = mp.get(fechas, fecha)
        dateAc = me.getValue(entry)
    else:
        dateAc = newDateAcquired(fecha)
        mp.put(fechas, fecha, dateAc)
    lt.addLast(dateAc["artworks"], artwork)


def addArtworkMedium(catalog, medium, artwork):
    """
    Adiciona una obra a la lista de obras que utilizaron una tecnica
    en especifico
    """
    mediums = catalog["mediums"]
    existMedium = mp.contains(mediums, medium)
    if existMedium:
        entry = mp.get(mediums, medium)
        tecnica = me.getValue(entry)
    else:
        tecnica = newMedium(medium)
        mp.put(mediums, medium, tecnica)
    lt.addLast(tecnica["artworks"], artwork)


def addArtworkNationality(catalog, nationality, artwork):
    """
    Adiciona una obra a la lista de obras que son de una nacionalidad
    en especifico
    """
    nationalities = catalog["nationalities"]
    existNationality = mp.contains(nationalities, nationality)
    if existNationality:
        entry = mp.get(nationalities, nationality)
        nacionalidad = me.getValue(entry)
    else:
        nacionalidad = newNationality(nationality)
        mp.put(nationalities, nationality, nacionalidad)
    lt.addLast(nacionalidad["artworks"], artwork)


# Funciones para creacion de datos

def newDateAcquired(fecha):
    """
    Crea una nueva estructura para modelar las obras de una fecha
    """
    dateAc = {"dateAcquired": "",
              "artworks": None}
    dateAc["dateAcquired"] = fecha
    dateAc["artworks"] = lt.newList("SINGLE_LINKED")
    return dateAc


def newNames(artwork, names):
    """
    Adiciona los nombres de los artistas a la obra dada por parametro
    """
    artwork["NombresArtistas"] = names


def newMedium(medium):
    """
    Crea una nueva estructura para modelar las obras de una tecnica
    """
    tecnica = {"medium": "",
               "artworks": None}
    tecnica["medium"] = medium
    tecnica["artworks"] = lt.newList("SINGLE_LINKED")
    return tecnica


def newNationality(nationality):
    """
    Crea una nueva estructura para modelar las nacionalidades de una obra
    """
    nacionalidad = {"nationality": "",
                    "artworks": None}
    nacionalidad["nationality"] = nationality
    nacionalidad["artworks"] = lt.newList("SINGLE_LINKED")
    return nacionalidad


# Funciones de consulta

def artworksRange(catalog, fecha1, fecha2):
    """
    Obtiene las obras de un rango de fechas y las almacena en un mapa, la
    cantidad de obras adquiridas por compra y la cantidad de obras del rango
    """
    artworks = catalog["artworks"]
    contador = 0
    total = 0
    for artwork in lt.iterator(artworks):
        fecha = artwork["DateAcquired"]
        if fecha == "":
            fecha = "2099-09-09"
        if fecha >= fecha1 and fecha <= fecha2:
            addArtworkRange(catalog, fecha, artwork)
            namesArtistsinArtworks(artwork, catalog["artists"])
            if "purchase" in artwork["CreditLine"].lower():
                contador += 1
            total += 1
    return mp.keySet(catalog["artDateAcquired"]), contador, total


def namesArtistsinArtworks(obra, artists):
    """
    Basados en los ConstituentIDs de los artistas, agrega los nombres a la
    lista de obras
    """
    id = obra["ConstituentID"]
    id = id.replace("[", "").replace("]", "").split(", ")
    nombres = lt.newList("ARRAY_LIST")
    for artista in id:
        for artist in lt.iterator(artists):
            if artista == artist["ConstituentID"]:
                lt.addLast(nombres, artist["DisplayName"])
                break
    artistas = ""
    for nombre in lt.iterator(nombres):
        artistas += nombre + ", "
    newNames(obra, artistas[:-2])


def constituentID(nombre, catalog):
    """
    Busca el ConstituentID de un artista, considerando el nombre dado
    """
    consID = None
    for artist in lt.iterator(catalog["artists"]):
        if nombre == artist["DisplayName"]:
            consID = artist["ConstituentID"]
            break
    return consID


def artistArtworks(constituentID, catalog):
    """
    Obtiene todas las obras de un artista y las almacena en un mapa de tecnicas
    """
    for artwork in lt.iterator(catalog["artworks"]):
        id = artwork["ConstituentID"]
        id = id.replace("[", "").replace("]", "").split(", ")
        for artista in id:
            if constituentID == artista:
                addArtworkMedium(catalog, artwork["Medium"], artwork)
    return catalog["mediums"]


def artistMedium(mapTecnicas):
    """
    Identifica la tecnica más utilizada en las obras de un artista, el numero
    total de tecnicas distintas que se usaron, y el numero total de obras
    """
    mayor = 0
    total = 0
    maximo = ""
    distintas = mp.size(mapTecnicas)
    tecnicas = mp.keySet(mapTecnicas)
    for tecnica in lt.iterator(tecnicas):
        pareja = mp.get(mapTecnicas, tecnica)
        obras = pareja["value"]["artworks"]
        cantObras = lt.size(obras)
        total += cantObras
        if cantObras > mayor:
            maximo = tecnica
            mayor = cantObras
    return maximo, distintas, total


def getArworksbyMedium(catalog, mediumName):
    """
    Retorna todas las obras dada una tecnica
    """
    medium = mp.get(catalog["mediums"], mediumName)
    if medium:
        return me.getValue(medium)
    return None


def nationalityArtistsinArtwork(artwork, artists):
    """
    Basados en los ConstituentIDs de los artistas, retorna las nacionalidades
    de una obra en especifico
    """
    artistas = artwork["ConstituentID"]
    artistas = artistas.replace("[", "").replace("]", "").split(", ")
    nacionalidades = lt.newList("ARRAY_LIST")
    for id in artistas:
        for artist in lt.iterator(artists):
            if id == artist["ConstituentID"]:
                artistNat = artist["Nationality"]
                if artistNat == "" or artistNat == "Nationality unknown":
                    artist["Nationality"] = "Unknown"
                lt.addLast(nacionalidades, artist["Nationality"])
                break
    return nacionalidades


def getArworksbyNationality(catalog, nationalityName):
    """
    Retorna todas las obras dada una nacionalidad
    """
    nacionalidad = mp.get(catalog["nationalities"], nationalityName)
    if nacionalidad:
        return me.getValue(nacionalidad)
    return None


# Funciones utilizadas para comparar elementos dentro de una lista

def cmpArtworkByDateAcquired(artwork1, artwork2):
    """
    Devuelve verdadero (True) si el "DateAcquired" de artwork1 es menor que
    el de artwork2
    Args:
        artwork1: informacion de la primera obra que incluye
                  unicamente su valor "DateAcquired"
        artwork2: informacion de la segunda obra que incluye
                  unicamente su valor "DateAcquired"
    """
    return artwork1 < artwork2


def cmpArtworkByDate(artwork1, artwork2):
    """
    Devuelve verdadero (True) si el "Date" de artwork1 es menor que
    el de artwork2
    Args:
        artwork1: informacion de la primera obra que incluye
                  su valor "TransCost"
        artwork2: informacion de la segunda obra que incluye
                  su valor "TransCost"
    """
    if artwork1["Date"] == "":
        date1 = 2099
    else:
        date1 = int(artwork1["Date"])
    if artwork2["Date"] == "":
        date2 = 2099
    else:
        date2 = int(artwork2["Date"])
    return date1 < date2


# Funciones de ordenamiento

def sortArtWorks(artworks, sizeArtworks):
    """
    Ordena las obras de arte por fecha de adquisicion
    """
    sub_list = lt.subList(artworks, 1, sizeArtworks)
    sub_list = sub_list.copy()
    sorted_list = ms.sort(sub_list, cmpArtworkByDateAcquired)
    return sorted_list


def sortDateArtworks(artworks, sizeArtworks):
    """
    Ordena las obras por la fecha de la obra
    """
    sub_list = lt.subList(artworks, 1, sizeArtworks)
    sub_list = sub_list.copy()
    sorted_list = ms.sort(sub_list, cmpArtworkByDate)
    return sorted_list


# Funciones de comparacion

def compareDateAcquired(keyname, fecha):
    """
    Compara dos fechas de adquisicion. El primero es una cadena de caracteres
    y el segundo un entry de un map
    """
    dateEntry = me.getKey(fecha)
    if (keyname == dateEntry):
        return 0
    elif (keyname > dateEntry):
        return 1
    else:
        return -1


def compareMedium(keyname, medium):
    """
    Compara dos tecnicas. El primero es una cadena de caracteres y el segundo
    un entry de un map
    """
    mediumEntry = me.getKey(medium)
    if (keyname == mediumEntry):
        return 0
    elif (keyname > mediumEntry):
        return 1
    else:
        return -1


def compareNationality(keyname, nationality):
    """
    Compara dos nacionalidades. El primero es una cadena de caracteres y el
    segundo un entry de un map
    """
    nationalityEntry = me.getKey(nationality)
    if (keyname == nationalityEntry):
        return 0
    elif (keyname > nationalityEntry):
        return 1
    else:
        return -1
