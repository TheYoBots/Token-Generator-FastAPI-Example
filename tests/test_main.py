import hashlib

from fastapi.testclient import TestClient

import main


client = TestClient(main.app)


def test_generate_single_token():
    resp = client.get("/generate")
    assert resp.status_code == 200
    data = resp.json()
    assert "token" in data
    assert isinstance(data["token"], str)
    assert len(data["token"]) >= 1


def test_tokens_post_checksum_and_tokens():
    text = "hello world"
    resp = client.post("/tokens", json={"text": text})
    assert resp.status_code == 200
    data = resp.json()
    assert "checksum" in data and "tokens" in data

    # Verify checksum is correct
    expected = hashlib.sha256(text.encode("utf-8")).hexdigest()
    assert data["checksum"] == expected

    # Tokens should be a non-empty list
    assert isinstance(data["tokens"], list)
    assert len(data["tokens"]) >= 1
