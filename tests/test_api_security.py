"""Security regression tests for the API compatibility server."""

from __future__ import annotations

from types import SimpleNamespace

from fastapi import HTTPException
import pytest

from perplexity_web_mcp.api import server


def test_server_config_defaults_to_loopback(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(server, "load_token", lambda: "session-token")
    for name in ("HOST", "PWM_API_KEY", "ANTHROPIC_API_KEY"):
        monkeypatch.delenv(name, raising=False)

    config = server.ServerConfig.from_env()

    assert config.host == "127.0.0.1"
    assert config.api_key is None


@pytest.mark.parametrize("host", ["0.0.0.0", "::", "192.168.1.25", "api.internal"])
def test_non_loopback_bind_requires_authentication(host: str) -> None:
    with pytest.raises(ValueError, match=r"Refusing to bind.*without authentication"):
        server.ServerConfig(session_token="session-token", host=host)


@pytest.mark.parametrize("host", ["127.0.0.1", "127.1.2.3", "::1", "[::1]", "localhost"])
def test_loopback_bind_allows_authentication_to_be_omitted(host: str) -> None:
    config = server.ServerConfig(session_token="session-token", host=host)
    assert config.api_key is None


def test_non_loopback_bind_accepts_explicit_api_key() -> None:
    config = server.ServerConfig(session_token="session-token", host="0.0.0.0", api_key=" strong-secret ")

    assert config.api_key == "strong-secret"


def test_pwm_api_key_is_used_for_server_auth(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(server, "load_token", lambda: "session-token")
    monkeypatch.setenv("HOST", "0.0.0.0")
    monkeypatch.setenv("PWM_API_KEY", "server-secret")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "legacy-secret")

    config = server.ServerConfig.from_env()

    assert config.api_key == "server-secret"


@pytest.mark.parametrize(
    ("headers", "accepted"),
    [
        ({"x-api-key": "server-secret"}, True),
        ({"Authorization": "Bearer server-secret"}, True),
        ({"Authorization": "bearer server-secret"}, True),
        ({"Authorization": "Basic server-secret"}, False),
        ({"x-api-key": "wrong"}, False),
        ({}, False),
    ],
)
def test_verify_auth_rejects_missing_or_invalid_credentials(
    headers: dict[str, str], accepted: bool, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(server, "config", SimpleNamespace(api_key="server-secret"), raising=False)
    request = SimpleNamespace(headers=headers)

    if accepted:
        server.verify_auth(request)
    else:
        with pytest.raises(HTTPException) as exc_info:
            server.verify_auth(request)
        assert exc_info.value.status_code == 401


def test_verify_auth_remains_optional_on_loopback_when_unconfigured(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(server, "config", SimpleNamespace(api_key=None), raising=False)
    server.verify_auth(SimpleNamespace(headers={}))
