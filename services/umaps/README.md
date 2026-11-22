# uMap + self-hosted tiles

Self-hosted [uMap](https://github.com/umap-project/umap) (your own "My Maps" — pins, layers, import/export GeoJSON/KML) **plus your own OpenStreetMap raster tiles** (TileServer GL), so the base map is self-hosted too. Reached over the tailnet via Tailscale Serve (HTTPS).

## Stack
`db` (PostGIS) · `redis` (realtime) · `app` (uMap, uvicorn/ASGI — does **not** serve static) · `nginx` (serves `/static/` + `/uploads/` + `/tiles/`, proxies the app) · `tileserver` (TileServer GL — raster tiles from an OpenMapTiles `.mbtiles`).

## Setup
1. `cp .env.example .env` → fill `SECRET_KEY`, `SITE_URL`/`TS_HOST` (your Tailscale host), `UMAP_DATA`, `TILES_DATA`.
2. `cp umap.conf.example "$UMAP_DATA/umap.conf"` → set `CSRF_TRUSTED_ORIGINS` to your host + map center/zoom.
3. Create dirs (uploads must be writable by uid 1000):
   ```bash
   sudo mkdir -p "$UMAP_DATA"/{db,uploads/ajax_cache,statics}
   sudo chown -R 1000:1000 "$UMAP_DATA/uploads"
   ```
4. `docker compose up -d`
5. Front with HTTPS: `sudo tailscale serve --bg 8001` → `https://<your-host>.ts.net`
6. Ensure that HTTPS origin is in `CSRF_TRUSTED_ORIGINS` (umap.conf) and `SITE_URL`, then `docker compose restart app`.
7. Create your account: `docker compose exec app umap createsuperuser`.

## Tiles
- Build an OpenMapTiles `.mbtiles` with [Planetiler](https://github.com/onthegomap/planetiler) (free, no account), e.g.:
  ```bash
  docker run --rm -e JAVA_TOOL_OPTIONS="-Xmx16g" -v "$TILES_DATA/..":/data \
    ghcr.io/onthegomap/planetiler:latest --download --area=europe --output=/data/europe.mbtiles
  ```
  Put the `.mbtiles` in `$TILES_DATA` (one file auto-loads).
- Find the style id: `curl -s https://<your-host>.ts.net/tiles/styles.json`.
- In uMap admin → **Tile layers** → URL: `https://<your-host>.ts.net/tiles/styles/<id>/{z}/{x}/{y}.png` (max zoom **20**). Must be **same-origin HTTPS** (served via nginx `/tiles/`) to avoid mixed-content blocking.

## Importing places (`scripts/`)
- `takeout_maps_to_umap.py` — flatten a Google Takeout Maps GeoJSON → clean uMap-ready GeoJSON (name + description).
- `geojson2kml.py` — convert a Point GeoJSON → KML (for CoMaps / Organic Maps / OsmAnd).

Run each with `python3 -I <script> <args>` (see the header in each file). Then import the GeoJSON into a uMap layer.

## Notes
- `$UMAP_DATA` (db/uploads/statics/umap.conf) and `$TILES_DATA` (.mbtiles) live on the host — **not** in this repo.
- Use the **full** `maptiler/tileserver-gl` image (not `-light`) — only the full one rasterizes to PNG.
- Tailnet-only; never expose publicly.
