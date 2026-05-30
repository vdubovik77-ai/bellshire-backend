# Bellshire Homes — Voice Assistant Backend

FastAPI backend for the Bellshire Homes AI consultation feature.

## Endpoints
- `GET /health` — healthcheck
- `POST /session` — issue ephemeral OpenAI Realtime token (WebRTC voice)
- `POST /sdp` — SDP offer proxy → OpenAI Realtime
- `POST /chat` — text chat completion (gpt-4o)
- `POST /extract`, `POST /analyze` — extract form fields + meetings from convo
- `POST /conversation/save` — persist convo to SQLite
- `GET /admin/conversations?token=...` — admin HTML view

## Deploy to Render
1. Push this folder to GitHub.
2. Render Dashboard → New → **Blueprint** → connect repo → it picks up `render.yaml`.
3. Set `OPENAI_API_KEY` in the Render env vars dashboard.
4. Wait for build. Service URL: `https://bellshire-backend.onrender.com`.

## Run locally
```bash
cp .env.example .env  # add OPENAI_API_KEY
.venv/bin/uvicorn main:app --reload --port 8000
```
