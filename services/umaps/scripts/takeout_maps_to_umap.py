# takeout_maps_to_umap.py — flatten a Google Takeout Maps GeoJSON into clean uMap-ready GeoJSON.
# Puts the place name at top-level "name" (so uMap labels pins) and folds address/comment/URL into "description".
# Usage (run from a neutral dir, data path passed as arg):
#   python3 -I takeout_maps_to_umap.py "<input.json>" "<output.geojson>"
import json, sys


def t(v):
    return v.strip() if isinstance(v, str) else ""


def build(feat):
    p = feat.get("properties") or {}
    loc = p.get("location") if isinstance(p.get("location"), dict) else {}
    name = t(p.get("name")) or t(loc.get("name")) or t(loc.get("address")) or t(p.get("address")) or "Unnamed place"
    addr = t(loc.get("address")) or t(p.get("address"))
    parts = []
    if addr:
        parts.append(addr)
    for k in ("Comment", "review_text_published"):
        if t(p.get(k)):
            parts.append(t(p.get(k)))
    if t(p.get("google_maps_url")):
        parts.append(t(p.get("google_maps_url")))
    if t(p.get("date")):
        parts.append("saved: " + t(p.get("date")))
    return {
        "type": "Feature",
        "geometry": feat.get("geometry"),
        "properties": {"name": name, "description": "\n".join(parts)},
    }


src, dst = sys.argv[1], sys.argv[2]
d = json.load(open(src, encoding="utf-8"))
feats = [build(f) for f in d.get("features", []) if (f.get("geometry") or {}).get("coordinates")]
json.dump({"type": "FeatureCollection", "features": feats},
          open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"{src}  ->  {dst}:  {len(feats)} features")
