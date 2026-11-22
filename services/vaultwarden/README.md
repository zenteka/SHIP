# Vaultwarden — self-hosted password manager (Bitwarden-compatible)

Your passwords, on your own hardware, E2E-encrypted, synced to all Bitwarden clients. **Requires HTTPS** → fronted by Tailscale Serve (here on port **8443**, since another service may own 443).

## 1. Deploy
```bash
cp .env.example .env          # set TS_HOST (your Tailscale URL) + VAULT_DATA (a data path OUTSIDE this repo)
sudo mkdir -p "$VAULT_DATA"   # the VAULT lives here — back it up, keep it out of git
docker compose up -d
```

## 2. Put it behind HTTPS (Tailscale Serve)
```bash
sudo tailscale serve --bg --https=8443 8084
sudo tailscale serve status        # should show https://${TS_HOST}:8443 -> 127.0.0.1:8084
```
(Each web service gets its own port; all get a `*.ts.net` cert.)

## 3. Create your account, then LOCK IT DOWN
1. Open **`${TS_HOST}`** → **Create account** (strong, unique master password — the one you must remember).
2. Disable new signups: set `SIGNUPS_ALLOWED: "false"` in `docker-compose.yml` → `docker compose up -d` again.
   (Re-enable briefly if you add family accounts.)

## 4. Connect your clients
Install **Bitwarden** (browser, iOS, Android, desktop) → before logging in, **Settings → Server URL** → `${TS_HOST}` → log in.
- ⚠️ Clients reach it only **on the tailnet** (a `*.ts.net` URL). Keep Tailscale running in the background on mobile so the vault's reachable. **Don't** expose it publicly (no Funnel) — keep it tailnet-only.

## 5. Optional — admin panel (/admin)
Set an admin token. Generate an Argon2 hash:
```bash
sudo docker run --rm vaultwarden/server /vaultwarden hash   # prompts for a password, prints the hash
```
Put it in `ADMIN_TOKEN` (compose env or `.env`) → restart → visit `${TS_HOST}/admin`.

## ⚠️ Backups — this is your password vault
- Everything is in `$VAULT_DATA` (SQLite `db.sqlite3` + attachments + keys) — on the host, **not** in this repo.
- **Back it up** (restic/borg → NAS / offsite). Losing it = losing all stored passwords.
- Keep your master password + 2FA recovery somewhere **offline** too.
- Migrating from Bitwarden cloud / a browser / LastPass? Export (JSON) → import in the Bitwarden web vault → shred the export.
