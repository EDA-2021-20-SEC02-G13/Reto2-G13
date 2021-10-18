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
 """

import config as cf
import model
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo
"""


# Inicialización del Catálogo de libros

def initCatalog():
    """
    Llama la funcion de inicializacion del catalogo del modelo
    """
    catalog = model.newCatalog()
    return catalog


# Funciones para la carga de datos

def loadData(catalog):
    """
    Carga los datos de los archivos y carga los datos en la estructura de datos
    """
    loadArtists(catalog)
    loadArtworks(catalog)
    loadMaps(catalog)


def loadArtists(catalog):
    """
    Carga todos los artistas del archivo al catalago del MoMA
    """
    artistfile = cf.data_dir + "MoMA/Artists-utf8-small.csv"
    input_file = csv.DictReader(open(artistfile, encoding="utf-8"))
    for artist in input_file:
        model.addArtist(catalog, artist)


def loadArtworks(catalog):
    """
    Carga todas las obras del archivo al catalago del MoMA
    """
    artworkfile = cf.data_dir + "MoMA/Artworks-utf8-small.csv"
    input_file = csv.DictReader(open(artworkfile, encoding="utf-8"))
    for artwork in input_file:
        model.addArtwork(catalog, artwork)


def loadMaps(catalog):
    """
    Carga los mapas que requieren que ambas listas ya esten creadas
    """
    model.addArtistArtwork(catalog)


# Funciones de ordenamiento

def sortArtists(artists, sizeArtists):
    """
    Ordena los artistas por fecha de nacimiento
    """
    return model.sortArtists(artists, sizeArtists)


def sortArtWorks(artworks, sizeArtworks):
    """
    Ordena las obras de arte por fecha de adquisicion
    """
    return model.sortArtWorks(artworks, sizeArtworks)


def sortDateArtworks(artworks, sizeArtworks):
    """
    Ordena las obras por la fecha de la obra
    """
    return model.sortDateArtworks(artworks, sizeArtworks)


# Funciones de consulta sobre el catálogo

def artworksRange(catalog, fecha1, fecha2):
    """
    Obtiene las obras de un rango de fechas, la cantidad de obras adquiridas
    por compra y la cantidad de obras del rango
    """
    return model.artworksRange(catalog, fecha1, fecha2)


def artistMedium(mapArtistas, nombre):
    """
    Identifica la tecnica más utilizada en las obras de un artista, el numero
    total de tecnicas distintas que se usaron, y el numero total de obras
    """
    return model.artistMedium(mapArtistas, nombre)


def getArworksbyMedium(catalog, mediumName, nombre):
    """
    Retorna todas las obras dada una tecnica
    """
    mediumInfo = model.getArworksbyMedium(catalog, mediumName, nombre)
    return mediumInfo


def getAuthorsByDate(catalog, anio1, anio2):
    """
    Retorna una lista de fechas dado un rango determinado por dos años
    """
    return model.getAuthorsByDate(catalog, anio1, anio2)


def getArworksbyNationality(catalog):
    """
    Retorna todas las obras dada una nacionalidad
    """
    nationalityInfo = model.getArworksbyNationality(catalog)
    return nationalityInfo


def getArtistByDate(catalog, anio1, anio2):
    """
    Retorna una lista de artistas dado un rango determinado por dos años
    """
    return model.getArtistByDate(catalog, anio1, anio2, )


def getprolificArtist(catalog, artists, size):
    """
    Retorna una lista ordenada con los artistas mas prolificos
    """
    return model.getprolificArtist(catalog, artists, size)
