# Quick Start — Clone, Install, Run

## 0. Ollama (local LLM — no API key)

Slide copy is generated with **[Ollama](https://ollama.com/)** via the Microsoft Agent Framework (`OllamaChatClient`). There is **no API key**; the backend talks to whatever model you run locally.

1. Install and start Ollama, then pull the default model (must match `OLLAMA_MODEL`, default `llama3.1:latest`):

   ```bash
   ollama pull llama3.1
   ollama serve
   ```

   `ollama serve` is often already running as a background service after install; if requests fail, start it explicitly.

2. Optional environment variables (no secrets):

   | Variable       | Default                      | Purpose                                      |
   | -------------- | ---------------------------- | -------------------------------------------- |
   | `OLLAMA_HOST`  | `http://localhost:11434`     | Ollama HTTP API base URL                     |
   | `OLLAMA_MODEL` | `llama3.1:latest`            | Model tag (`ollama list` after pulling)     |

   When the API runs **inside Docker** and Ollama is on your machine, set `OLLAMA_HOST` to `http://host.docker.internal:11434` (see `docker-compose.yml`).

3. Optional sanity check (from `backend/`):

   ```bash
   python smoke_ollama_agent.py
   ```

   You should see a short greeting printed. If Ollama reports insufficient **system RAM** for `llama3.1`, pull a smaller model and set `OLLAMA_MODEL` to that tag, or free memory on the host.

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

Verify the backend API docs at:

```text
http://localhost:8000/docs
```
