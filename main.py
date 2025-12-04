"""FastAPI app for generating pseudorandom tokens and computing text checksums.

This small app demonstrates:
- an interactive HTML form (served at `/`) to submit text and request tokens
- an API endpoint `POST /tokens` that accepts JSON {"text": "..."} and returns
  a checksum and a list of pseudorandom tokens
- a helper `GET /generate` endpoint that returns a single token

This file includes inline documentation and comments intended to guide GitHub
Copilot-style assistants for learning and demonstration purposes.
"""
from typing import List
import hashlib
import secrets
import base64

from fastapi.responses import Response

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.responses import Response

app = FastAPI(title="Token Generator API", description="Generate tokens and checksums")
templates = Jinja2Templates(directory="templates")


def generate_token() -> str:
    """Generate a single pseudorandom token.

    Uses `secrets.token_hex` for cryptographically strong random tokens.
    """
    return secrets.token_hex(16)


# Small 1x1 PNG used as a favicon (base64 encoded). This keeps the repo file-free
# while ensuring requests to `/favicon.ico` return a valid image instead of 404.
_FAVICON_PNG_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMAASsJTYQAAAAA"
    "SUVORK5CYII="
)
_FAVICON_BYTES = base64.b64decode(_FAVICON_PNG_B64)


@app.get("/favicon.ico")
async def favicon():
    """Return a tiny PNG as the favicon to avoid 404s from browsers."""
    return Response(content=_FAVICON_BYTES, media_type="image/png")


# Serve a rocket image at /static/rocket.png. The content is SVG (so browsers
# will render it) but it's exposed at the PNG path to match the requested URL
# and to behave like a file resource in the templates.
@app.get("/static/rocket.png")
async def rocket_image():
        svg = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 512 512' width='220' height='220' aria-hidden='true'>
    <g>
        <path d='M186 256c0 0-42-86 68-198 110 112 68 198 68 198s-56 16-136 0z' fill='#ff4d6d'/>
        <path d='M256 96c0 0 64 24 104 72 40 48 40 112 40 112s-56 16-144 16-144-16-144-16 0-64 40-112C192 120 256 96 256 96z' fill='#ff6f91' opacity='0.95'/>
        <circle cx='326' cy='172' r='28' fill='#a6ecff'/>
        <path d='M156 400c-20-12-36-28-48-48l56-40 56 40-56 48z' fill='#ff8a65'/>
        <path d='M256 384c0 28-24 56-56 56s-56-28-56-56 24-56 56-56 56 28 56 56z' fill='#ffb74d' opacity='0.9'/>
    </g>
</svg>"""
        return Response(content=svg, media_type="image/svg+xml")


# Create a Pydantic model to accept JSON with a single `text` field
# GitHub Copilot hint: generate a Pydantic model named `TextIn` with one field `text: str`.
class TextIn(BaseModel):
    text: str


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Render a simple HTML form to submit text and call the API.

    The template demonstrates how a user (Mark) can interact with the API using
    a browser. A welcome message is included for the participant.
    """
    # Use the specific welcome and quote text to match the design requirements.
    welcome = "Welcome to the webpage, Jaya Narayana!"
    return templates.TemplateResponse("index.html", {"request": request, "welcome": welcome})


@app.get("/generate")
async def single_generate():
    """Return a single pseudorandom token as JSON.

    This mirrors the original single-token endpoint described in the activity.
    """
    token = generate_token()
    return JSONResponse({"token": token})


# GitHub Copilot hint: create a FastAPI POST endpoint called `/tokens` that accepts
# a JSON body with field `text` and returns a checksum of the text.
@app.post("/tokens")
async def tokens_endpoint(payload: TextIn):
    """Accept JSON {"text": "..."} and return checksum and a list of tokens.

    Response format:
    {
      "checksum": "<sha256-hex>",
      "tokens": ["token1", "token2", ...]
    }

    Implementation notes:
    - Checksum is computed using SHA-256 of the raw `text` bytes.
    - We generate one pseudorandom token per word in the text (as a simple example).
    """
    text = payload.text or ""

    # Compute checksum (SHA-256 hex digest)
    checksum = hashlib.sha256(text.encode("utf-8")).hexdigest()

    # Generate a token for each whitespace-separated word. If there are no words,
    # generate a single token so the response always contains at least one token.
    words = [w for w in text.split() if w]
    count = max(1, len(words))
    tokens: List[str] = [secrets.token_hex(8) for _ in range(count)]

    return JSONResponse({"checksum": checksum, "tokens": tokens})


if __name__ == "__main__":
    # Simple run guard for local execution with `python main.py` (not required when using uvicorn).
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
