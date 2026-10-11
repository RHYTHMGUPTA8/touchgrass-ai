# TouchGrass AI 🌿

**A local-first outdoor mission generator powered by an open-weight language model.** TouchGrass turns a few free minutes into a practical real-world activity, then gets out of the way. No account, cloud AI API, streaks, or social feed.

> Hacktoberfest theme: Touch Grass — the screen should be the shortest part of the experience.

## Why open innovation matters

- **Privacy by default:** the user's preferences are sent to the Ollama process running on their own machine, not to a hosted model API.
- **Works without internet after setup:** download the app dependencies and model once; mission generation then runs locally. The PWA caches its static shell, but generating a new mission still requires the local Ollama service.
- **Model choice:** `OLLAMA_MODEL` can be changed to another compatible model. The prompt and safety constraints are visible and editable.
- **Accessible experimentation:** contributors can run, inspect, test, and extend the project without paying per-token API fees.

The model is open-weight, and the application code is MIT-licensed. Model licenses vary; check the license of any model you choose before redistributing it.

## Features

- AI-generated missions tailored by activity, time, energy, setting, accessibility needs, and things to avoid.
- Local inference through Ollama; no hosted AI API key.
- Responsive UI with checklist, mindfulness prompt, and a concise safety reminder.
- Local-only mission title history in browser storage.
- Installable PWA shell with cached static assets.
- FastAPI backend, request validation, health endpoint, and basic tests.

## Quick start (local)

### 1. Install Ollama and download a model

Install [Ollama](https://ollama.com/) for your operating system, then run:

```bash
ollama pull qwen2.5:3b
```

Keep Ollama running. The model is downloaded once; the app makes requests to its local API.

### 2. Set up the application

Python 3.10+ is recommended.

```bash
git clone https://github.com/YOUR-USERNAME/touchgrass-ai.git
cd touchgrass-ai
python -m venv .venv
```

Activate the environment:

- Windows PowerShell: `\.venv\Scripts\Activate.ps1`
- macOS/Linux: `source .venv/bin/activate`

Install and run:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open [http://localhost:8000](http://localhost:8000). API docs are at [http://localhost:8000/docs](http://localhost:8000/docs).

### Configuration

Copy `.env.example` to `.env` as a reference. The app does not automatically load `.env`; export the variables in your shell or configure them in your IDE/runtime.

PowerShell:

```powershell
$env:OLLAMA_URL="http://localhost:11434"
$env:OLLAMA_MODEL="qwen2.5:3b"
uvicorn app.main:app --reload
```

macOS/Linux:

```bash
export OLLAMA_URL=http://localhost:11434
export OLLAMA_MODEL=qwen2.5:3b
uvicorn app.main:app --reload
```

Use a model that fits your machine's memory and compute. Smaller quantized models generally run more comfortably on laptops.

## Docker option

The included Compose file starts the app and Ollama service. After starting the services, pull the model into the Ollama container:

```bash
docker compose up -d --build
docker compose exec ollama ollama pull qwen2.5:3b
```

Then open [http://localhost:8000](http://localhost:8000). The first model download requires internet. Later inference is local. Resource use depends on your hardware and model choice.

## Tests

```bash
pip install -r requirements.txt
pytest -q
```

## API

- `GET /api/health` — service/model configuration status.
- `POST /api/mission` — generate a mission.

Example request:

```json
{
  "activity": "birdwatching",
  "duration": 20,
  "energy": "low",
  "setting": "park",
  "accessibility": "Prefer a flat path",
  "avoid": "Crowds"
}
```

The response is structured JSON with a title, reason, 3–5 checklist steps, mindfulness prompt, safety note, and estimated duration.

## Safety and limitations

TouchGrass is not a navigation, emergency, medical, or wildlife-identification tool. Check local weather and trail/park rules, stay in public areas, and choose an activity appropriate for your surroundings and abilities. Do not touch or feed wildlife or eat unknown plants. Model output can be imperfect; use common sense and skip anything unsafe.

The app does not currently provide GPS, maps, weather checks, or fully offline AI on its own. Local inference is offline only after Ollama and the model have been installed and downloaded.

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md). Good first contributions include more accessible mission templates, automated tests, improved local model setup, translations, and better offline UX.

## License

MIT — see [LICENSE](LICENSE).
