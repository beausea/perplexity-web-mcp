"""AI model definitions."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Model:
    """AI model configuration."""

    identifier: str
    mode: str = "copilot"


class Models:
    """Available AI models (all use copilot mode with web search)."""

    DEEP_RESEARCH = Model(identifier="pplx_alpha")
    """Deep Research - Create in-depth reports with more sources, charts, and advanced reasoning."""

    CREATE_FILES_AND_APPS = Model(identifier="pplx_beta")
    """Create files and apps (previously known as Labs) - Turn your ideas into docs, slides, dashboards, and more."""

    BEST = Model(identifier="pplx_pro")
    """Best - Automatically selects the best model based on the query."""

    SONAR = Model(identifier="experimental", mode="concise")
    """Sonar 2 — Perplexity's latest in-house model (backend id: experimental)."""

    GEMINI_31_PRO_THINKING = Model(identifier="gemini31pro_high")
    """Gemini 3.1 Pro Thinking - Google's most advanced model (thinking)."""

    GPT_54 = Model(identifier="gpt54")
    """GPT-5.4 - OpenAI's versatile model."""

    GPT_54_THINKING = Model(identifier="gpt54_thinking")
    """GPT-5.4 Thinking - OpenAI's versatile model (thinking)."""

    GPT_55 = Model(identifier="gpt55")
    """GPT-5.5 - OpenAI's latest model (Max only)."""

    GPT_55_THINKING = Model(identifier="gpt55_thinking")
    """GPT-5.5 Thinking - OpenAI's latest model with thinking (Max only)."""

    CLAUDE_50_SONNET = Model(identifier="claude50sonnet")
    """Claude Sonnet 5.0 - Anthropic's fast model."""

    CLAUDE_50_SONNET_THINKING = Model(identifier="claude50sonnetthinking")
    """Claude Sonnet 5.0 Thinking - Anthropic's newest reasoning model."""

    CLAUDE_48_OPUS = Model(identifier="claude48opus")
    """Claude Opus 4.8 - Anthropic's most advanced reasoning model."""

    CLAUDE_48_OPUS_THINKING = Model(identifier="claude48opusthinking")
    """Claude Opus 4.8 Thinking - Anthropic's most advanced reasoning model (thinking)."""

    NEMOTRON_3_ULTRA = Model(identifier="nv_nemotron_3_ultra")
    """Nemotron 3 Ultra - NVIDIA's Nemotron 3 Ultra 550B model (thinking)."""

    GLM_5_2 = Model(identifier="glm_5_2")
    """GLM-5.2 - Z.ai's advanced model (thinking)."""

    KIMI_K2_6 = Model(identifier="kimik26instant")
    """Kimi K2.6 - Moonshot AI's latest model."""

    KIMI_K2_6_THINKING = Model(identifier="kimik26thinking")
    """Kimi K2.6 Thinking - Moonshot AI's latest model (thinking)."""
