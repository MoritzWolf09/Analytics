#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Python3-Klasse zur Berechnung von geografischen Koordinaten
aus REGNIE-Rasterzellen.

Es ist eine 'main'-Methode zum Testen der Klasse enthalten.



Aufbau des REGNIE-Rasters
-------------------------
Das Gitter besteht aus
611 Rasterpunkten in West/Ost-Richtung und
971 Rasterpunkten in Nord/Süd-Richtung.

Die Auflösung beträgt
60 geogr. Sekunden längenparallel und
30 geogr. Sekunden breitenparallel, d.h.
1 Längengrad setzt sich aus 60 Gitterpunkten,
1 Breitengrad aus 120 Gitterpunkten zusammen.


Berechnung der geogr. Koordinaten der Rasterpunkte:

Schrittweite längenparallel
    (xdelta) : 60 geogr. Sekunden
    xdelta = 1.0 * (1./60.) (Grad)

Schrittweite breitenparallel
    (ydelta) : 30 geogr. Sekunden
    ydelta = 1.0 * (1./120.) (Grad)


Geogr. Koordinaten des Rasterpunktes R(1,1) links oben:
x(1,1) =  6. - 10.*xdelta
y(1,1) = 55. + 10.*ydelta

Geogr. Koordinaten eines beliebigen Rasterpunktes R(m,n):
x(m,n) = ( 6. - 10.*xdelta) + (n - 1)*xdelta
y(m,n) = (55. + 10.*ydelta) - (m - 1)*ydelta,

wobei x in West/Ost-Richtung ( n von 1 bis 611 )
  und y in Nord/Süd-Richtung ( m von 1 bis 971 ) verläuft.

Bezug:
Jede Koordinate bezieht sich auf den Mittelpunkt der REGNIE-Zelle.

erstellt am 29.08.2013
@author: Deutscher Wetterdienst, Abteilung Hydrometeorologie, Mario Hafer, KU42

Version: 29.03.2017
'''

class RegnieCoords:
    '''
    classdocs
    '''
    
    
    #
    #    Statisch - muss nur ein mal berechnet werden
    #
    
    xdelta_grad = 1.0 /  60.0
    ydelta_grad = 1.0 / 120.0
    
    
    
    """
    def __init__(self):
        '''
        Constructor
        '''
    """
    
    
    
    @staticmethod
    def convertPixelToGeographicCoordinates(cartesian_point_regnie): # y, x
        """ Berechnungsfunktion """
        
        lat = (55.0 + 10.0 * RegnieCoords.ydelta_grad) - (cartesian_point_regnie[0] - 1) * RegnieCoords.ydelta_grad
        lon = ( 6.0 - 10.0 * RegnieCoords.xdelta_grad) + (cartesian_point_regnie[1] - 1) * RegnieCoords.xdelta_grad
        
        return lat, lon







if __name__ == '__main__':
    """ TEST """
    
    #print RegnieCoords.xdelta_grad
    #print RegnieCoords.ydelta_grad
    
    
    #
    #    Pixel festlegen
    #
    
    # Erstes Pixel oben links:
    p1 = (1, 1)
    
    # 611 Rasterpunkten in West/Ost-Richtung und
    # 971 Rasterpunkten in Nord/Süd-Richtung
    p2 = (971, 1)
    
    # Pixel sammeln:
    pixel = [ p1, p2 ]
    
    
    #
    #    Berechnen
    #
    
    for p in pixel:
        lat, lon = RegnieCoords.convertPixelToGeographicCoordinates(p)
        print( str(p) + ": ", lat, lon)
    