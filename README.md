# Token Generator FastAPI Example

This small example demonstrates a FastAPI application that:

- Serves an interactive HTML form at `/` to submit text and request tokens.
- Provides `GET /generate` to return a single pseudorandom token.
- Provides `POST /tokens` to accept JSON `{"text": "..."}` and return:
  - `checksum`: SHA-256 hex digest of the text
  - `tokens`: a list of pseudorandom tokens (one per word by default)

Prerequisites
-------------

- Python 3.10+ recommended
- Create and activate a virtual environment

Install dependencies
--------------------

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the app (development)
-------------------------

Start the server with `uvicorn`:

```bash
uvicorn main:app --reload
```

Open your browser to `http://127.0.0.1:8000/` to use the interactive form.

API usage
---------

- `GET /generate` — returns JSON: `{ "token": "..." }`
- `POST /tokens` — send JSON body `{ "text": "your text" }` and receive:

```json
{
  "checksum": "<sha256-hex>",
  "tokens": ["...", "..."]
}
```

Tests
-----

Run tests with:

```bash
pytest -q
```
