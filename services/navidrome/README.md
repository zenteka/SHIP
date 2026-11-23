# Navidrome — self-hosted music streaming

Stream your own music library to any device (iPhone, laptop, browser) over the tailnet — **nothing stored on the client**. [Subsonic-API](https://www.subsonic.org/) compatible, so a wide range of apps work.

## Design
- Your **music library stays outside this service** (shared, Syncthing-synced, also used by other tools), mounted **read-only** — Navidrome scans + streams, never writes.
- Only Navidrome's **own small DB/cache** (`$NAVIDROME_DATA`) belongs to the service.
- **Storage tiers:** library on **HDD** (streaming is sequential + cheap/TB); Navidrome's DB on **SSD** (snappier scans). Don't put music on SSD.

## Setup
1. `cp .env.example .env` → set `MUSIC_DIR` (your library), `NAVIDROME_DATA`, and `PUID`/`PGID` (a user that can read the library).
2. `sudo mkdir -p "$NAVIDROME_DATA"`.
3. `docker compose up -d` → first run scans the library.
4. Front with HTTPS: `sudo tailscale serve --bg 4533` → `https://<your-host>.ts.net`.
5. Open it → create your admin account.

## Clients (stream, store nothing)
Point a Subsonic client at `https://<your-host>.ts.net` + your Navidrome login:
- **iOS:** **Amperfy** (open-source) ⭐ · play:Sub · substreamer
- **Android:** Symfonium · Tempo · DSub
- **Desktop/Web:** the built-in web UI, or Feishin.

With Tailscale running on the device you can stream **anywhere** (even on cellular). Caching albums for **offline** is opt-in — by default nothing is stored on the phone.

## Save mobile data
Navidrome transcodes on the fly — set a lower bitrate per client (Settings → Transcoding) so a FLAC library streams light over cellular.

## Notes
- `$MUSIC_DIR` + `$NAVIDROME_DATA` live on the host — **not** in this repo.
- The library mount is **read-only** — your files + their Syncthing sync stay the source of truth.
- **Tailnet-only** — don't expose publicly.
