#!/bin/bash

# ./snake.sh waterbody.geojson 20
#
# Note this only makes a buffered geometry of the *first* geometry
# given in the INPUTFILE as the first argument. Adjust the SQL statement
# as appropriate or parameterize it as needed

INPUTFILE="$1"
LAYER=${INPUTFILE%.*}
BUFFER=$2
rm buffered.*
CPL_DEBUG=ON ogr2ogr buffered.shp $LAYER.geojson  -sql "SELECT ST_Buffer(ST_Union(a.geometry), $BUFFER) from $LAYER a where rowid=0" -dialect "SQLITE"
ogrinfo buffered.shp -sql "ALTER TABLE buffered ADD COLUMN InBuffer integer(2)"
ogrinfo buffered.shp -dialect SQLite -sql "UPDATE buffered set InBuffer = 1"

rm union.*
CPL_DEBUG=ON ogr2ogr union.shp $LAYER.geojson \
    -sql "SELECT
    ST_BuildArea(ST_Union(CastToXY(a.geometry)))
        from $LAYER a where rowid=0" -dialect "SQLITE"
