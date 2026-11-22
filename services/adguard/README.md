# AdGuard Home — network-wide ad / tracker blocking

Runs a DNS server on your always-on server; point Tailscale at it → **every device on your tailnet gets ad/tracker filtering**, with no per-device setup.

## Why DNS is bound to specific IPs
Linux's `systemd-resolved` already holds `127.0.0.53:53`, so binding AdGuard to `0.0.0.0:53` would clash. Binding instead to the server's **tailnet IP** (`${TAILNET_IP}`) and **LAN IP** (`${LAN_IP}`) avoids the conflict with **no changes to the host's DNS**. *(If a bind still fails, check what's on :53 with `sudo ss -lntup 'sport = :53'`.)*

## Setup
1. `cp .env.example .env` and fill in your values (tailnet IP, LAN IP, data path).
2. Create the data dir + deploy:
   ```bash
   sudo mkdir -p "$ADGUARD_DATA/work" "$ADGUARD_DATA/conf"
   docker compose up -d
   docker compose logs -f adguardhome      # Ctrl-C to stop watching
   ```

## First-run wizard
Open `http://<TAILNET_IP>:3000` (or `http://<LAN_IP>:3000`):
- **Admin Web Interface** → listen on *All interfaces*, port **3000** (keeps it on the published port).
- **DNS server** → listen on *All interfaces*, port **53**.
- Create your admin username + password.

## Configure
- **Upstream DNS** (Settings → DNS settings): use a private, ideally encrypted resolver — e.g. DoH `https://dns.quad9.net/dns-query` or `https://cloudflare-dns.com/dns-query`.
- **Blocklists** (Filters → DNS blocklists): the default list is on; add more (OISD, HaGeZi, StevenBlack, plus any regional lists).

## Point your whole tailnet at it (the step that makes it network-wide)
Tailscale admin console → **DNS → Nameservers → Add nameserver → Custom** → `${TAILNET_IP}` → enable **Override local DNS**.
Now every Tailscale device resolves through AdGuard → filtering everywhere, even on mobile data. Verify in the dashboard **Query Log**.

## Notes
- Over-blocked a site? Find it in the Query Log → add to the allowlist.
- Data lives in `$ADGUARD_DATA` (config + stats) on the host — **not** in this repo.
- Keep it **tailnet-only** — never expose the DNS (`53`) or admin (`3000`) ports to the public internet.
- DNS-level blocking can't stop first-party/same-domain ads; pair with a browser content blocker for those.
