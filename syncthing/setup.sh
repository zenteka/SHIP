#!/usr/bin/env bash
#
# Install Syncthing on Debian/Ubuntu and run it as a per-user systemd service.
#
# Syncthing keeps a shared folder (e.g. ~/main) in sync across your devices —
# peer-to-peer, offline-first, no cloud. It is NOT a Docker service; it runs
# natively on each device. Run this once per machine.
#
# Docs: https://docs.syncthing.net/
set -euo pipefail

# 1. Official Syncthing apt repo (newer + maintained vs. the distro package) ----
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://syncthing.net/release-key.gpg \
  | sudo tee /etc/apt/keyrings/syncthing.gpg >/dev/null
echo "deb [signed-by=/etc/apt/keyrings/syncthing.gpg] https://apt.syncthing.net/ syncthing stable" \
  | sudo tee /etc/apt/sources.list.d/syncthing.list >/dev/null
sudo apt-get update
sudo apt-get install -y syncthing

# 2. Enable it for the current user (starts at boot, no desktop login needed) ---
sudo systemctl enable --now "syncthing@${USER}.service"

cat <<MSG

Syncthing is installed and running as user '${USER}'.

Next steps (do these in the Web UI — http://127.0.0.1:8384):
  1. Note THIS device's ID (Actions -> Show ID).
  2. On each of your other devices, add this ID (and add theirs here).
  3. Share the folder you want synced (e.g. ~/main), set it to 'Send & Receive'.

Headless server (e.g. over Tailscale)? The Web UI binds to 127.0.0.1 only.
Reach it with an SSH tunnel:
    ssh -L 8384:127.0.0.1:8384 <server>     # then open http://127.0.0.1:8384
Set a GUI user/password before exposing it any wider.
MSG
