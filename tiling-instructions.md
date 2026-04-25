Install gdal tools:
```bash
$ apt list --installed|grep -i gdal

gdal-bin/jammy,now 3.4.1+dfsg-1build4 amd64 [installed]
gdal-data/jammy,jammy,now 3.4.1+dfsg-1build4 all [installed,automatic]
libgdal-dev/jammy,now 3.4.1+dfsg-1build4 amd64 [installed]
libgdal30/jammy,now 3.4.1+dfsg-1build4 amd64 [installed]
python3-gdal/jammy,now 3.4.1+dfsg-1build4 amd64 [installed,automatic]
```

# Crop and reduce cells to 8 bit values
# Moscow metro area bounds-
# 56.06414845228367, 37.05557480995671
# 55.31603441970138, 38.4739442000234

```bash
gdal_translate \
   -ot Byte \
   -of GTiff \
   -projwin 37.05557480995671 56.06414845228367 \
            38.4739442000234 55.31603441970138 \
   data/rus_pop_2026_CN_100m_R2025A_v1.tif \
   data/tmp-moscow-metro-ru.tif
```

# Generate tiles
```bash
# Generate tiles
nice -n 19 gdal2tiles.py --processes=6 -z 0-10 -w none data/tmp-moscow-metro-ru.tif ./tiles/
```

```bash
gdalwarp \
  -t_srs EPSG:3857 \
  -r bilinear \
  data/tmp-moscow-metro-ru.tif \
  data/tmp-moscow-metro-ru-3857.tif
```  

# Run local webserver to serve tiles

```bash
python3 -m http.server 8000
```

# Presumably this is the URL format spec for retrieving tiles
http://localhost:8000/tiles/{z}/{x}/{y}.png

Tiles are getting requested, but the z-x-y coords don't exist in ./tiles

# Colors pipeline:

# 1. Reproject (if needed)
gdalwarp -t_srs EPSG:3857 input.tif warped.tif

# 2. Normalize values
gdal_translate -scale 0 3000 0 255 warped.tif scaled.tif

# 3. Apply color map
gdaldem color-relief scaled.tif colors.txt colored.tif



# Server correction

# 1. Crop using lat/lon safely
gdal_translate \
  -projwin_srs EPSG:4326 \
  -projwin 37.0556 56.0641 38.4739 55.3160 \
  input.tif cropped.tif

# 2. Reproject to Web Mercator
gdalwarp \
  -t_srs EPSG:3857 \
  -r bilinear \
  cropped.tif cropped_3857.tif

# 3. Generate XYZ tiles
gdal2tiles.py \
  --xyz \
  -z 0-10 \
  cropped_3857.tif \
  ./tiles/


# Combined

# 1. Crop to Moscow metro area, project to 4326, reduce values to byte-sized
gdal_translate \
   -ot Byte \
   -of GTiff \
   -projwin_srs EPSG:4326 \
   -projwin 37.05557480995671 56.06414845228367 \
            38.4739442000234 55.31603441970138 \
   data/rus_pop_2026_CN_100m_R2025A_v1.tif \
   data/tmp-moscow-metro-ru-espg4326.tif

# 2. Generate color-relief version
gdaldem color-relief \
  data/tmp-moscow-metro-ru-espg4326.tif \
  colors2.txt \
  data/tmp-moscow-metro-ru-espg4326-colored2.tif

# 3. Reproject to Web Mercator
gdalwarp \
  -t_srs EPSG:3857 \
  -r bilinear \
  data/tmp-moscow-metro-ru-espg4326-colored2.tif \
  data/tmp-moscow-metro-ru-espg3857-colored2-warped.tif

# 4. Generate XYZ tiles
gdal2tiles.py \
  --xyz \
  -z 0-10 \
  data/tmp-moscow-metro-ru-espg3857-colored2-warped.tif \
  ./tiles/


# Must run the SPA from localhost and specify the tiles format URL as follows:
http://localhost:8000/index009.html
http://localhost:8000/tiles/{z}/{x}/{y}.png


# The last run which functioned 24 April 2026
# 1. Crop to Moscow metro area, project to 4326, reduce values to byte-sized
gdal_translate \
    -ot Byte \
    -of GTiff \
    -projwin_srs EPSG:4326 \
    -projwin 37.05557480995671 56.06414845228367 \
             38.4739442000234 55.31603441970138 \
    data/rus_pop_2026_CN_100m_R2025A_v1.tif \
    data/tmp-moscow-metro-ru-espg4326.tif

# 2. Generate color-relief version
gdaldem color-relief \
   data/tmp-moscow-metro-ru-espg4326.tif \
   colors2.txt \
   data/tmp-moscow-metro-ru-espg4326-colored2.tif

# 3. Reproject to Web Mercator
gdalwarp \
   -t_srs EPSG:3857 \
   -r bilinear \
   data/tmp-moscow-metro-ru-espg4326-colored2.tif \
   data/tmp-moscow-metro-ru-espg3857-colored2-warped.tif

# 4. Generate XYZ tiles
gdal2tiles.py \
   --xyz \
   -z 0-10 \
   data/tmp-moscow-metro-ru-espg3857-colored2-warped.tif \
   ./tiles/
