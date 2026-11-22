# Syncthing — device sync

**Not a Docker service.** Syncthing runs *natively* on each device and keeps a shared
folder in sync between them — peer-to-peer, offline-first, end-to-end encrypted in
transit, no cloud and no central server. It's the glue that lets the same files follow
me across machines (this repo itself lives inside the synced folder).

## The idea

```
  laptop ◄─────────► server ◄─────────► phone
         Syncthing          Syncthing
            \                  /
             └──► ~/main ◄────┘      (same folder, everywhere; offline-first)
```

- One folder (here: `~/main`) is shared between all devices, set to **Send & Receive**.
- Each device holds a full local copy, so everything works **offline**; changes
  reconcile automatically whenever two devices can see each other (incl. over a
  Tailscale tailnet).
- There is no "master" — any device can edit; Syncthing versions and merges.

## Setup

Run once per machine:

```bash
./setup.sh
```

It installs Syncthing from the official apt repo and enables the per-user systemd
service (`syncthing@<user>.service`). Then, in the Web UI at `http://127.0.0.1:8384`:

1. Copy **this device's ID** (Actions → Show ID).
2. On your other devices, **add that ID** (and add theirs here) — devices must
   approve each other.
3. **Share the folder** (e.g. `~/main`) and set it to **Send & Receive**.

## Headless / server

The Web UI binds to `127.0.0.1` only. To reach a server's UI, tunnel it:

```bash
ssh -L 8384:127.0.0.1:8384 <server>   # then open http://127.0.0.1:8384
```

Set a GUI username/password before exposing the UI any wider than localhost.

## Notes

- **Device IDs and folder config are per-device and are *not* committed** — only this
  setup script and notes live in git.
- Don't sync live databases or a `.git` index you also commit from elsewhere — sync
  source files and documents, not state that two machines mutate concurrently.
- Back up the shared folder independently; sync is replication, **not** a backup
  (a delete propagates everywhere). Syncthing's file-versioning helps, but isn't a
  substitute for real backups.
