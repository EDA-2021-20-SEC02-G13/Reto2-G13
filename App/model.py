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

from DISClib.DataStructures.arraylist import addLast
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
               "dates": None,
               "artDateAcquired": None,
               "artistsMediums": None,
               "nationalities": None,
               "departments": None}

    catalog["artists"] = lt.newList("SINGLE_LINKED")

    catalog["artworks"] = lt.newList("SINGLE_LINKED")

    catalog["dates"] = mp.newMap(235,
                                 maptype="PROBING",
                                 loadfactor=0.5,
                                 comparefunction=compareBeginDate)

    catalog["artDateAcquired"] = mp.newMap(32800,
                                           maptype="PROBING",
                                           loadfactor=0.5,
                                           comparefunction=compareDateAcquired)

    catalog["artistsMediums"] = mp.newMap(15223,
                                          maptype="PROBING",
                                          loadfactor=0.5,
                                          comparefunction=compareArtist)

    catalog["nationalities"] = mp.newMap(118,
                                         maptype="PROBING",
                                         loadfactor=0.5,
                                         comparefunction=compareNationality)

    catalog["departments"] = mp.newMap(8,
                                       maptype="PROBING",
                                       loadfactor=0.5,
                                       comparefunction=compareDepartment)

    return catalog


# Funciones para agregar informacion al catalogo

def addArtist(catalog, artist):
    """
    Adiciona un artista a la lista de artistas, la cual guarda referencias
    a la informacion de dicho artista
    """
    lt.addLast(catalog["artists"], artist)
    addAuthorDate(catalog, artist, artist["BeginDate"])


def addArtwork(catalog, artwork):
    """
    Adiciona una obra a lista de obras, la cual guarda referencias a la
    informacion de dicha obra
    """
    lt.addLast(catalog["artworks"], artwork)
    nacionalidades = nationalityArtistsinArtwork(artwork, catalog["artists"])
    for nacionalidad in lt.iterator(nacionalidades):
        addArtworkNationality(catalog, nacionalidad, artwork)
    addArtworkRange(catalog, artwork["DateAcquired"], artwork)
    addArtworkDepartment(catalog, artwork["Department"], artwork)
    namesArtistsinArtworks(artwork, catalog["artists"])


def addAuthorDate(catalog, artist, date):
    """
    Adiciona una obra a la lista de artistas que son de una fecha de nacimiento
    en especifico
    """
    dates = catalog["dates"]
    existDate = mp.contains(dates, date)
    if existDate:
        entry = mp.get(dates, date)
        fecha = me.getValue(entry)
    else:
        fecha = newBeginDate(date)
        mp.put(dates, date, fecha)
    lt.addLast(fecha["artists"], artist)


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


def addArtistArtwork(catalog):
    """
    Agrega las obras de un artista a un mapa, donde las llaves son los artistas
    y los valores sus obras y los medios utilizados
    """
    for artist in lt.iterator(catalog["artists"]):
        consID = artist["ConstituentID"]
        name = artist["DisplayName"]
        for artwork in lt.iterator(catalog["artworks"]):
            id = artwork["ConstituentID"]
            id = id.replace("[", "").replace("]", "").split(", ")
            for artista in id:
                if consID == artista:
                    medium = artwork["Medium"]
                    addArtworkMedium(catalog, medium, artwork, name, consID)


def addArtworkMedium(catalog, medium, artwork, name, consID):
    """
    Adiciona una obra a la lista de obras que utilizaron una tecnica en
    especifico y a las obras de un artista
    """
    artists = catalog["artistsMediums"]
    existArtist = mp.contains(artists, name)
    if existArtist:
        entry = mp.get(artists, name)
        artista = me.getValue(entry)
    else:
        artista = newArtistMedium(name, consID)
        mp.put(artists, name, artista)
    lt.addLast(artista["artworks"], artwork)
    addMedium(artista, medium, artwork)


def addMedium(artista, medium, artwork):
    """
    Adiciona una obra a la lista de obras que utilizaron una tecnica
    en especifico
    """
    mediums = artista["mediums"]
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


def addArtworkDepartment(catalog, department, artwork):
    """
    Adiciona una obra a la lista de obras que son de un departamento
    en especifico
    """
    departamentos = catalog["departments"]
    existDepartment = mp.contains(departamentos, department)
    if existDepartment:
        entry = mp.get(departamentos, department)
        departamento = me.getValue(entry)
    else:
        departamento = newDepartment(department)
        mp.put(departamentos, department, departamento)
    lt.addLast(departamento["artworks"], artwork)


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


def newBeginDate(fecha):
    """
    Crea una nueva estructura para modelar las obras de una fecha de nacimiento
    """
    beginDate = {"beginDate": "",
                 "artists": None}
    beginDate["beginDate"] = fecha
    beginDate["artists"] = lt.newList("SINGLE_LINKED")
    return beginDate


def newArtistMedium(name, consID):
    """
    Crea una nueva estructura para modelar las obras de un artista y tecnica
    """
    artista = {"artist": "",
               "consID": "",
               "artworks": None,
               "mediums": mp.newMap(50,
                                    maptype="PROBING",
                                    loadfactor=0.5,
                                    comparefunction=compareMedium)}
    artista["artist"] = name
    artista["consID"] = consID
    artista["artworks"] = lt.newList("SINGLE_LINKED")
    return artista


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


def newDepartment(department):
    """
    Crea una nueva estructura para modelar los departamentos de una obra
    """
    dept = {"department": "",
            "artworks": None}
    dept["department"] = department
    dept["artworks"] = lt.newList("SINGLE_LINKED")
    return dept


def newCosts(artwork, costs):
    """
    Adiciona los costos de transporte a la obra dada por parametro
    """
    artwork["TransCost"] = costs


def newBonusInfo(artist, obras, tecnicas, topMedium):
    """
    Adiciona los nombres de los artistas a la obra dada por parametro
    """
    artist["ArtworkNumber"] = obras
    artist["MediumNumber"] = tecnicas
    artist["TopMedium"] = topMedium


# Funciones de consulta

def artworksRange(catalog, fecha1, fecha2):
    """
    Obtiene las obras de un rango de fechas, la cantidad de obras adquiridas
    por compra y la cantidad de obras del rango
    """
    fechas = catalog["artDateAcquired"]
    datesArtworks = lt.newList("ARRAY_LIST")
    contador = 0
    total = 0
    for fecha in lt.iterator(mp.keySet(fechas)):
        if fecha >= fecha1 and fecha <= fecha2:
            lt.addLast(datesArtworks, fecha)
            pareja = mp.get(fechas, fecha)
            artworks = pareja["value"]["artworks"]
            for artwork in lt.iterator(artworks):
                total += 1
                if "purchase" in artwork["CreditLine"].lower():
                    contador += 1
    return datesArtworks, contador, total


def namesArtistsinArtworks(artwork, artists):
    """
    Basados en los ConstituentIDs de los artistas, agrega los nombres a la
    lista de obras
    """
    id = artwork["ConstituentID"]
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
    newNames(artwork, artistas[:-2])


def artistMedium(mapArtistas, nombre):
    """
    Identifica la tecnica más utilizada en las obras de un artista, el numero
    total de tecnicas distintas que se usaron, y el numero total de obras
    """
    mayor = 0
    maximo = ""
    pareja = mp.get(mapArtistas, nombre)
    obras = pareja["value"]["artworks"]
    tecnicas = pareja["value"]["mediums"]
    consID = pareja["value"]["consID"]
    distintas = lt.size(mp.keySet(tecnicas))
    for tecnica in lt.iterator(mp.keySet(tecnicas)):
        pareja2 = mp.get(tecnicas, tecnica)
        artworks = pareja2["value"]["artworks"]
        cantObras = lt.size(artworks)
        if cantObras > mayor:
            maximo = tecnica
            mayor = cantObras
    return maximo, distintas, lt.size(obras), consID


def getArworksbyMedium(catalog, mediumName, nombre):
    """
    Retorna todas las obras dada una tecnica
    """
    mapArtistas = catalog["artistsMediums"]
    artista = mp.get(mapArtistas, nombre)
    mapTecnicas = artista["value"]["mediums"]
    medium = mp.get(mapTecnicas, mediumName)
    if medium:
        return me.getValue(medium)
    return None


def getAuthorsByDate(catalog, anio1, anio2):
    """
    Retorna una lista de fechas dado un rango determinado por dos años
    """
    dates = catalog["dates"]
    datesArtists = lt.newList("ARRAY_LIST")
    contador = 0
    for anio in lt.iterator(mp.keySet(dates)):
        if anio >= anio1 and anio <= anio2:
            lt.addLast(datesArtists, anio)
            pareja = mp.get(dates, anio)
            artists = pareja["value"]["artists"]
            for artist in lt.iterator(artists):
                contador += 1
    return datesArtists, contador


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


def getArworksbyNationality(catalog):
    """
    Retorna todas las obras dada una nacionalidad
    """
    lista_xd = lt.newList('ARRAY_LIST')
    nationalityName = mp.keySet(catalog['nationalities'])
    for nationality in lt.iterator(nationalityName):
        nacionalidad = mp.get(catalog["nationalities"], nationality)
        lt.addLast(lista_xd, me.getValue(nacionalidad))
    return lista_xd


def artworksDepartment(catalog, departamento):
    """
    Obtiene todas las obras que estan ligadas a un departamento, el costo
    para cada obra, y el costo y peso total del departamento
    """
    mapDepartment = catalog["departments"]
    pareja = mp.get(mapDepartment, departamento)
    obras = pareja["value"]["artworks"]
    Tipo_Medida = lt.newList('ARRAY_LIST')
    addLast(Tipo_Medida,'Circumference (cm)')
    addLast(Tipo_Medida,'Depth (cm)')
    addLast(Tipo_Medida,'Diameter (cm)')
    addLast(Tipo_Medida,'Height (cm)')
    addLast(Tipo_Medida,'Length (cm)')
    addLast(Tipo_Medida,'Width (cm)')
    addLast(Tipo_Medida,'Seat Height (cm)')
    costoDpta = 0
    kgDpta = 0
    for artwork in lt.iterator(obras):
        costoArea = 0
        costoVolumen = 0
        if artwork["Weight (kg)"] == "":
            costokg = 0
        else:
            costokg = float(artwork["Weight (kg)"]) * 72
            kgDpta += float(artwork["Weight (kg)"])
        for medida in lt.iterator(Tipo_Medida):
            try:
                metros = float(artwork[medida])/100
                artwork[medida] = metros
            except:
                metros = 0
                artwork[medida] = metros
        if artwork['Depth (cm)'] != 0:
            costoVolumen = artwork["Depth (cm)"] * artwork["Height (cm)"] * artwork["Width (cm)"] * 72
        elif (artwork["Height (cm)"] and artwork["Width (cm)"]) != 0:
            costoArea = artwork["Height (cm)"] * artwork["Width (cm)"]* 72
        elif (artwork['Depth (cm)'] and artwork["Height (cm)"] and artwork["Width (cm)"]) == 0:
            costoVolumen = 48
        elif (artwork["Height (cm)"] and artwork["Width (cm)"]) == 0:
            costoArea = 48
        
            



        costoTotal = max(costokg, costoArea, costoVolumen)
        newCosts(artwork, round(costoTotal, 3))
        costoDpta += costoTotal
    return obras, costoDpta, kgDpta


def getArtistByDate(catalog, anio1, anio2):
    """
    Retorna una lista de artistas dado un rango determinado por dos años
    """
    dates = catalog["dates"]
    datesArtists = lt.newList("ARRAY_LIST")
    for anio in lt.iterator(mp.keySet(dates)):
        if anio >= anio1 and anio <= anio2:
            pareja = mp.get(dates, anio)
            artists = pareja["value"]["artists"]
            for artist in lt.iterator(artists):
                lt.addLast(datesArtists, artist)
    return datesArtists


def getprolificArtist(catalog, artists, size):
    """
    Retorna una lista ordenada con los artistas mas prolificos
    """
    mapArtistas = catalog["artistsMediums"]
    for artist in lt.iterator(artists):
        nombre = artist["DisplayName"]
        pareja = mp.get(mapArtistas, nombre)
        if pareja is None:
            obras = 0
            tecnicas = 0
            mediums = (None, None)
        else:
            obras = lt.size(pareja["value"]["artworks"])
            tecnicas = mp.size(pareja["value"]["mediums"])
            mediums = artistMedium(catalog["artistsMediums"], nombre)
        newBonusInfo(artist, obras, tecnicas, mediums[0])
    return sortArtistArtworks(artists, size)


# Funciones utilizadas para comparar elementos dentro de una lista

def cmpArtistByBeginDate(artist1, artist2):
    """
    Devuelve verdadero (True) si el "BeginDate" de artist1 es menor que
    el de artist2
    Args:
        artist1: informacion del primer artista que incluye
                 unicamente su valor "BeginDate"
        artist2: informacion del segundo artista que incluye
                 unicamente su valor "BeginDate"
    """
    return int(artist1) < int(artist2)


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


def cmpArtistByCant(artist1, artist2):
    """
    Devuelve verdadero (True) si el "ArtworkNumber" de artist1 es mayor que
    el de artist2
    Args:
        artist1: informacion del primer artista que incluye
                 unicamente su valor "ArtworkNumber"
        artist2: informacion del segundo artista que incluye
                 unicamente su valor "ArtworkNumber"
    """
    if artist1["ArtworkNumber"] == artist2["ArtworkNumber"]:
        return artist1["MediumNumber"] > artist2["MediumNumber"]
    else:
        return artist1["ArtworkNumber"] > artist2["ArtworkNumber"]


# Funciones de ordenamiento

def sortArtists(artists, sizeArtists):
    """
    Ordena los artistas por fecha de nacimiento
    """
    sub_list = lt.subList(artists, 1, sizeArtists)
    sub_list = sub_list.copy()
    sorted_list = ms.sort(sub_list, cmpArtistByBeginDate)
    return sorted_list


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


def sortArtistArtworks(artists, cantidad):
    """
    Ordena los artistas por cantidad de obras y medios
    """
    sub_list = lt.subList(artists, 1, cantidad)
    sub_list = sub_list.copy()
    sorted_list = ms.sort(sub_list, cmpArtistByCant)
    return sorted_list


# Funciones de comparacion

def compareBeginDate(keyname, fecha):
    """
    Compara dos fechas de nacimiento. El primero es una cadena de caracteres
    y el segundo un entry de un map
    """
    dateEntry = me.getKey(fecha)
    if (keyname == dateEntry):
        return 0
    elif (keyname > dateEntry):
        return 1
    else:
        return -1


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


def compareArtist(keyname, artist):
    """
    Compara dos artistas. El primero es una cadena de caracteres y el segundo
    un entry de un map
    """
    artistEntry = me.getKey(artist)
    if (keyname == artistEntry):
        return 0
    elif (keyname > artistEntry):
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


def compareDepartment(keyname, department):
    """
    Compara dos departamentos. El primero es una cadena de caracteres y el
    segundo un entry de un map
    """
    departmentEntry = me.getKey(department)
    if (keyname == departmentEntry):
        return 0
    elif (keyname > departmentEntry):
        return 1
    else:
        return -1
