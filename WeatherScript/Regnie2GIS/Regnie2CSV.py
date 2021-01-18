#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Regnie2CSV
==========
Bereitet eine originale REGNIE-Rasterdatei
zur Verwendung in einem GIS auf.
Erzeugt aus dem originären Raster eine CSV-Datei für den GIS-Input.

Aufruf des Scripts:
-------------------
(python3) Regnie2CSV.py [-a][-j] <Regnie-Rasterfile>
[] = optional
-a: alles, auch Fehlwerte rausschreiben. Führt zu einer großen Ausgabedatei.
-j: eine kleine CSV-Datei schreiben, die nur die Daten und eine ID-Spalte
    enthält. Mittels ID können die Daten mit einem Shapefile kombiniert werden.
-------------------

Als weiterer Bestandteil des Scripts wird die Klasse 'RegnieCoords'
eingebunden.

                        - - -

REGNIE
------
Abspeicherung der Rasterfelder:
zeilenweise von Nord nach Süd und West nach Ost.

Algorithmus:

VON 1 bis (einschl.) 971:
    VON 1 bis (einschl.) 611:
        INTEGER = READ(4 Stellen)

Nichtbesetzte Rasterpunkte sind mit dem Fehlwert -999 besetzt.

Bezug:
Die ausgegebenen CSV-Koordinaten beziehen sich auf den Mittelpunkt
der REGNIE-Zelle.

Die Dimension der monatlichen und jährlichen Niederschlagshöhen beträgt mm,
die der täglichen mm/10.

CSV
---
Nichtbesetzte Rasterpunkte sind mit dem Wert -1 besetzt
(negative Werte treten sonst nicht auf).


erstellt am 29.08.2013
@author: Deutscher Wetterdienst, Abteilung Hydrometeorologie, Mario Hafer, KU42

Version: 29.03.2017
'''


import os
import sys
#sys.path.append("../../lib")    # nur damit Script auch im Test in Eclipse läuft
#from lib.coords.RegnieCoords import RegnieCoords
from RegnieCoords import RegnieCoords




NEWLINE_LEN = 1
"""
Standard 1
Unter Windows erstellte Textfiles (die Rasterdatei) haben idR zwei Zeichen
für einen Zeilenumbruch (\r\n).
Es wurde mit zwei Files getestet, für die allerdings die Linux-Codierung
(1 Zeichen, \n) verwendet wurde.
"""

# REGNIE-Ausdehnung:
Y_MAX = 971
X_MAX = 611


# Programmverhalten
ignore_missings = True      # Kleinere Datei erzeugen, also Fehlwerte überspringen
#ignore_missings = False    # Alle Werte rausschreiben
"""
Es sind recht viele Fehlwerte in den Regnie-Rastern enthalten; es macht daher
Sinn, diese Werte zu Gunsten kleinerer Ausgabedateien nicht rauszuschreiben.
-> etwa 7,5 MB gegenüber 13 MB
"""



def create_full_csv(fn_in, fn_out):
    """ Vollständige CSV-Datei mit Koordinaten, einer ID und den Werten erzeugen """
    
    f_in = open(fn_in, "r")
    
    f_out = open(fn_out, "w")
    f_out.write("LAT,LON,ID,VAL\n")    # Kopfzeile
    
    
    # Beginn mit Zelle...
    _id = 1             # für Vergleich mit Regnie-Polygonen im GIS eingeführt
    
    
    # Beginn mit 1 und Ende + 1, um REGNIE-konforme Pixelindizes zu erhalten
    for y in range(1, Y_MAX+1):
        
        for x in range(1, X_MAX+1):
            
            i_val = int(f_in.read(4))
            
            if i_val < 0:   # In Ursprungs-Rasterdatei: -999
                if ignore_missings: continue
                i_val = -1  # weiter mit diesem Wert
            
            point = (y,x)
            lat, lon = RegnieCoords.convertPixelToGeographicCoordinates(point)
            #f_out.write( "%f,%f,%d\n" % (lat, lon, i_val) )        # ohne _id
            f_out.write( "%f,%f,%d,%d\n" % (lat, lon, _id, i_val) )
            _id += 1
        
        # for x
            
        # Zeile vollständig:
        f_in.read(NEWLINE_LEN)
        print(".", end="")   # zu viele Pixel, daher nur 'for y'
        
    # for y
    
    print()
    
    f_in.close()
    f_out.close()
    




def create_join_csv(fn_in, fn_out):
    """ Erstellt eine kleine CSV-Datei, die nur die Daten und eine ID-Spalte
    enthält. Mittels ID können die Daten mit einem Shapefile kombiniert werden. """
    
    print("Erzeuge CSV-Joinfile...")
    
    f_in = open(fn_in, "r")
    
    f_out = open(fn_out, "w")
    f_out.write("ID,VAL\n")    # Kopfzeile
    
    
    # Beginn mit Zelle...
    _id = 1
    
    
    # Beginn mit 1 und Ende + 1, um REGNIE-konforme Pixelindizes zu erhalten
    for _ in range(1, Y_MAX+1):
        for _ in range(1, X_MAX+1):
            
            i_val = int(f_in.read(4))
            
            if i_val < 0:   # In Ursprungs-Rasterdatei: -999
                if ignore_missings: continue
                i_val = -1  # weiter mit diesem Wert
            
            f_out.write("{},{}\n".format(_id, i_val) )
            _id += 1
        
        # Zeile vollständig:
        f_in.read(NEWLINE_LEN)        # Rasterdatei hat Windows-Zeilenumbrüche, deswegen 2 Zeichen lesen (\r\n)
        print(".", end="")   # zu viele Pixel, daher nur 'for y'
    
    print()
    
    f_in.close()
    f_out.close()
    





def print_error_exit(msg=None):
    ''' Gibt eine übergebene Meldung aus,
    beschreibt den Aufruf des Programms
    und beendet das Programm. '''
    
    if msg:
        print(msg + "\n")
    
    print("""\
Anwendung des Scripts:
{} [-a][-j] <Regnie-Rasterfile>
[] = optional
-a: alles, auch Fehlwerte rausschreiben. Führt zu einer großen Ausgabedatei.
-j: eine kleine CSV-Datei schreiben, die nur die Daten und eine ID-Spalte enthält.
    Mittels ID-Feld können die Daten mit einem Regnie-Polygon-Shapefile kombiniert werden.
    """.format( os.path.basename(sys.argv[0]) ) )
    sys.exit()
    


if __name__ == '__main__':
    
    csv_join_mode = False
    
    # Argumente:
    # argv[0] = Scriptname
    # argv[1] = Join-Option oder Regnie-Rasterfile
    # argv[2] = nicht belegt oder Regnie-Rasterfile
    
    if len(sys.argv) < 2:
        print_error_exit()
    
    regnie_fn = None
    
    for arg in sys.argv:
        if arg == "-j":
            csv_join_mode = True
        elif arg == "-a":
            ignore_missings = False
            print("Es wurde angegeben, dass auch nichtbelegte Werte rausgeschrieben werden (Wert -1).")
            print("Achtung: dies führt zu einer größeren Ausgabedatei.")
        else:
            regnie_fn = arg
    
    
    if not regnie_fn or not os.path.exists(regnie_fn):
        print_error_exit("REGNIE-Inputfile '{}' wurde nicht gefunden!".format(regnie_fn))
    
    
    
    raster_fn_without_ext = os.path.splitext(regnie_fn)[0]
    
    
    
    """
    Entsprechende Funktion wählen:
    """
    
    # Standard:
    if not csv_join_mode:
        csv_fn = raster_fn_without_ext + "_full.csv"
        create_full_csv(regnie_fn, csv_fn)
    
    else:
        csv_fn = raster_fn_without_ext + "_join.csv"
        create_join_csv(regnie_fn, csv_fn)
    
    
    
    if not os.path.exists(csv_fn):
        print("Fehler beim Erstellen der CSV-Datei!\n", file=sys.stderr)
        sys.exit(1)
    
    
    print("-> {}".format(csv_fn))
    print()
    print("Ausgabe der Werte als Integer; bitte Skalierung des Produkts beachten!")
    print("Die Dimension der monatlichen und jährlichen Niederschlagshöhen beträgt mm,"
        + " die der täglichen mm/10.")
    
    
    
directory = r'C:\Users\lezi\GitHub\Analytics\weather-data\leipzig'
for filename in os.listdir(directory):
     print(filename)