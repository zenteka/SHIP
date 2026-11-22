# geojson2kml.py — convert a Point GeoJSON into a KML bookmark file for CoMaps / Organic Maps / OsmAnd.
# Usage: python3 -I geojson2kml.py <input.geojson> <output.kml> "<Category name>"
import json, sys
from xml.sax.saxutils import escape

src, dst, docname = sys.argv[1], sys.argv[2], sys.argv[3]
d = json.load(open(src, encoding="utf-8"))
out = ['<?xml version="1.0" encoding="UTF-8"?>',
       '<kml xmlns="http://www.opengis.net/kml/2.2">', '<Document>',
       f'  <name>{escape(docname)}</name>']
n = 0
for f in d.get("features", []):
    g = f.get("geometry") or {}
    if g.get("type") != "Point":
        continue
    c = g.get("coordinates")
    if not c or len(c) < 2:
        continue
    lon, lat = c[0], c[1]
    p = f.get("properties") or {}
    name = escape(str(p.get("name", "") or "Unnamed"))
    desc = escape(str(p.get("description", "") or ""))
    out.append(
        f'  <Placemark><name>{name}</name><description>{desc}</description>'
        f'<Point><coordinates>{lon},{lat}</coordinates></Point></Placemark>'
    )
    n += 1
out.append('</Document>')
out.append('</kml>')
open(dst, "w", encoding="utf-8").write("\n".join(out))
print(f"{src} -> {dst}: {n} placemarks")
