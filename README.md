# Quick Start — Clone, Install, Run

## 0. Ollama (LLM — no API key)

Slide copy is generated with **[Ollama](https://ollama.com/)** over its HTTP API (`/api/generate`): a planner builds an outline, then a writer fills each slide. There is **no API key**.

How you run Ollama depends on the path below:

- **Docker / Azure Container Apps:** Ollama runs **inside the backend container** (see `backend/Dockerfile` and `backend/docker-entrypoint.sh`). The app uses **`OLLAMA_HOST=http://127.0.0.1:11434`**. You do **not** install or host Ollama separately.
- **Local `uvicorn` dev:** Install Ollama on your machine and run it (or use its tray/service). Defaults: `OLLAMA_HOST=http://localhost:11434`, `OLLAMA_MODEL=llama3.1:latest`.

### Docker / production backend image

- **Single container** starts **`ollama serve`** in the background, waits until `http://127.0.0.1:11434/api/tags` responds, then runs **FastAPI** via `agent_main.py` (uvicorn on **`0.0.0.0`**, port from **`PORT`** env or **8000**).
- During **`docker build`**, the image runs a short-lived Ollama and executes **`ollama pull llama3.1:latest`** so the model is **baked into the image** (large download and layer).
- **Azure Container Apps:** Deploy this backend image; configure ingress to the container port (typically **8000**, or match **`PORT`** if your revision sets it). Ollama stays **internal** to the container on **11434** — you usually only expose **8000** publicly. Ensure the revision has **enough CPU/RAM** for the pulled model (e.g. Llama 3.1 is several GiB at runtime).

```bash
docker compose build backend
docker compose up backend
```

### Local development (host Ollama)

1. Install Ollama, pull the model (must match `OLLAMA_MODEL`):

   ```bash
   ollama pull llama3.1
   ollama serve
   ```

2. Optional environment variables (no secrets):

   | Variable       | Default (local dev)      | Purpose                          |
   | -------------- | ------------------------ | -------------------------------- |
   | `OLLAMA_HOST`  | `http://localhost:11434` | Ollama HTTP API base URL         |
   | `OLLAMA_MODEL` | `llama3.1:latest`        | Model tag (`ollama list`)        |

3. Optional sanity check (from `backend/` with venv active — hits `GET /api/tags`):

   ```bash
   python smoke_ollama_agent.py
   ```

   If Ollama reports insufficient **system RAM**, use a smaller model and set `OLLAMA_MODEL` accordingly.

## 1. Clone

```bash
git clone <repo-url>
cd slide-gen-workshop
```

## 2. Backend (Python)

```bash
cd backend
```

### Create virtual environment and activate (Windows)

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Or macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run backend (development)

```bash
uvicorn main:app --reload
```

## 3. Frontend (JavaScript)

Open a new terminal:

```bash
cd frontend
npm install
npm run dev
```

## 4. Environment

- Backend default: `http://localhost:8000`
- Frontend (Vite) default: `http://localhost:5173`

## 5. Verify the app

Open the frontend URL shown by Vite (usually `http://localhost:5173`).

Backend API docs:

```text
http://localhost:8000/docs
```
