# Vaultwarden on alia — self-hosted password manager (Bitwarden-compatible)

Your passwords, on your hardware, E2E-encrypted, synced to all Bitwarden clients. **Requires HTTPS** → fronted by Tailscale Serve on **port 8443** (uMap already owns 443, so Vaultwarden gets its own port).

## 1. Deploy (on alia)
```bash
sudo mkdir -p /mnt/storage/vaultwarden/data                          # the VAULT (NOT in the synced folder — back it up)
cd /mnt/storage/main/services_for_alia/vaultwarden                   # the ~/main folder syncs to here on alia
sudo docker compose up -d
```

## 2. Put it behind HTTPS (Tailscale Serve, extra port alongside uMap)
```bash
sudo tailscale serve --bg --https=8443 8084
sudo tailscale serve status        # should show https://${TS_HOST}:8443 -> 127.0.0.1:8084
```
(uMap stays on 443; Vaultwarden is on 8443. Both get the *.ts.net cert.)

## 3. Create your account, then LOCK IT DOWN
1. Open **https://${TS_HOST}:8443** → **Create account** (strong, unique master password — this one you must remember).
2. Then disable new signups: edit `docker-compose.yml` → `SIGNUPS_ALLOWED: "false"` → `sudo docker compose up -d`.
   (Re-enable briefly later if you add family accounts.)

## 4. Connect your clients
Install the **Bitwarden** app/extension (browser, iOS, Android, desktop) → before logging in, tap **Settings → Server URL** → `https://${TS_HOST}:8443` → then log in.
- ⚠️ Clients reach it only **on the tailnet** (it's a *.ts.net URL). Keep **Tailscale running in the background** on your phone so the vault is always reachable. (Do NOT expose it publicly via Funnel — keep the vault tailnet-only.)

## 5. Optional — admin panel (/admin)
To manage users/settings, set an admin token. Generate an Argon2 hash:
```bash
sudo docker run --rm vaultwarden/server /vaultwarden hash      # prompts for a password, prints the hash
```
Put the hash in `ADMIN_TOKEN` in the compose env → restart → visit `.../admin`.

## ⚠️ Backups — this is your password vault
- Everything is in `/mnt/storage/vaultwarden/data` (SQLite `db.sqlite3` + attachments + keys).
- **Back it up** (restic/borg → later the NAS/node 2). Losing it = losing all stored passwords.
- Keep your master password + the 2FA recovery somewhere offline too.
- Migrating from a browser/Google/LastPass? Export from the old one → import in the Bitwarden web vault → delete the export file.
