With gdal2tiles.py, how to debug when tiles aren't appearing as expected? I generated a cropped population map for the Moscow metro area, with the following workflow-

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
  colors.txt \
  data/tmp-moscow-metro-ru-espg4326-colored.tif

# 3. Reproject to Web Mercator
gdalwarp \
  -t_srs EPSG:3857 \
  -r bilinear \
  data/tmp-moscow-metro-ru-espg4326-colored.tif \
  data/tmp-moscow-metro-ru-espg3857-colored-warped.tif

# 4. Generate XYZ tiles
gdal2tiles.py \
  --xyz \
  -z 0-10 \
  data/tmp-moscow-metro-ru-espg4326-colored.tif \
  ./tiles/


The js SPA web app (index009.html) accessing the tiles is a MapLibre GL JS app that has a url format parameter pointing to the :8000 http tile server, "http://localhost:8000/tiles/{z}/{x}/{y}.png", and the JS is making requests to that server using that format, it's just that the z/x/y coordinates aren't always matching any of the tile files.
python3 -m http.server 8000
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
127.0.0.1 - - [24/Apr/2026 16:37:09] "GET /tiles/9/309/159.png HTTP/1.1" 200 -
127.0.0.1 - - [24/Apr/2026 16:37:09] "GET /tiles/9/308/159.png HTTP/1.1" 200 -
127.0.0.1 - - [24/Apr/2026 16:37:09] "GET /tiles/9/309/160.png HTTP/1.1" 200 -
127.0.0.1 - - [24/Apr/2026 16:37:09] "GET /tiles/9/308/160.png HTTP/1.1" 200 -
127.0.0.1 - - [24/Apr/2026 16:37:09] "GET /tiles/9/310/159.png HTTP/1.1" 200 -
127.0.0.1 - - [24/Apr/2026 16:37:09] "GET /tiles/9/310/160.png HTTP/1.1" 200 -
127.0.0.1 - - [24/Apr/2026 16:37:09] code 404, message File not found
127.0.0.1 - - [24/Apr/2026 16:37:09] "GET /tiles/9/309/161.png HTTP/1.1" 200 -
127.0.0.1 - - [24/Apr/2026 16:37:09] "GET /tiles/9/308/158.png HTTP/1.1" 404 -
127.0.0.1 - - [24/Apr/2026 16:37:09] code 404, message File not found
127.0.0.1 - - [24/Apr/2026 16:37:09] code 404, message File not found
127.0.0.1 - - [24/Apr/2026 16:37:09] code 404, message File not found
127.0.0.1 - - [24/Apr/2026 16:37:09] code 404, message File not found
127.0.0.1 - - [24/Apr/2026 16:37:09] "GET /tiles/9/309/158.png HTTP/1.1" 404 -
127.0.0.1 - - [24/Apr/2026 16:37:09] "GET /tiles/9/310/158.png HTTP/1.1" 404 -
127.0.0.1 - - [24/Apr/2026 16:37:09] "GET /tiles/9/307/160.png HTTP/1.1" 404 -
127.0.0.1 - - [24/Apr/2026 16:37:09] "GET /tiles/9/307/159.png HTTP/1.1" 404 -
127.0.0.1 - - [24/Apr/2026 16:37:09] "GET /tiles/9/310/161.png HTTP/1.1" 200 -
127.0.0.1 - - [24/Apr/2026 16:37:09] "GET /tiles/9/308/161.png HTTP/1.1" 200 -
127.0.0.1 - - [24/Apr/2026 16:37:09] code 404, message File not found
Looking for changesm
