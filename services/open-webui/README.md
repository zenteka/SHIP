# Open WebUI

A self-hosted web frontend for **local LLMs**. It talks to a local [Ollama](https://ollama.com)
instance and gives you a ChatGPT-style UI over your own models — nothing leaves the host.

> **Optional service.** This is only useful if you run local LLMs (Ollama) on the host.
> If you don't, skip it.

## How it's wired

- **Ollama** runs *natively* on the host (not in Docker) as a systemd service, listening on
  `0.0.0.0:11434`, with models under `/mnt/storage/ollama-models`.
- **Open WebUI** runs as a container on the **host network**, so it reaches Ollama at
  `localhost:11434` and serves its UI directly on **host port `8080`**.
- UI data (accounts, chats, settings) persists in the Docker named volume **`open-webui`**.

```
browser ──▶ http://<host>:8080  ──▶ Open WebUI (container, host net)
                                         └──▶ Ollama (native) localhost:11434
```

## Prerequisites

- Docker + Docker Compose on the host.
- Ollama installed and running with `OLLAMA_HOST=0.0.0.0:11434` and at least one model pulled
  (`ollama pull llama3.2`, etc.).

## Run

```bash
docker compose up -d
```

Then open `http://<host>:8080` (on this tailnet, front it with Tailscale Serve for HTTPS).

## Notes

- This compose file **reproduces** an earlier ad-hoc `docker run`. The `open-webui` volume is
  pinned by name, so switching to compose **reuses the existing data** rather than starting empty.
- Image tag is `:main` (rolling). Pin to a release tag if you want reproducible upgrades.
- `network_mode: host` is deliberate (lets the container reach the host's Ollama); because of it,
  do not add a `ports:` block — the UI is already on host `:8080`.
