# Contributing to TouchGrass AI

Thanks for helping people spend more time in the real world! Please keep contributions useful, accessible, and aligned with the project's local-first principles.

## Before opening a PR

1. Open or comment on an issue describing the change and why it helps.
2. Keep changes focused; avoid adding trackers, accounts, social feeds, or unnecessary screen-time loops.
3. Never introduce a hosted AI API as a required dependency. Optional providers should be clearly labeled and opt-in.
4. Do not commit API keys, `.env` files, model weights, or personal data.
5. Add or update tests and documentation for behavior changes.

## Development

```bash
python -m venv .venv
# Activate the environment, then:
pip install -r requirements.txt
pytest -q
uvicorn app.main:app --reload
```

Ollama and a compatible model are needed to manually test mission generation. API validation and homepage tests can run without the model service.

## Pull requests

Please include: the problem being solved, a short description of the change, how you tested it, and screenshots for visible UI changes. Be respectful and assume good intent in reviews.
