"""Gemini Embedding implementation."""

from __future__ import annotations

import os
from typing import Any, List, Optional

import httpx

from src.libs.embedding.base_embedding import BaseEmbedding


class GeminiEmbeddingError(RuntimeError):
    """Raised when Gemini Embeddings API call fails."""


class GeminiEmbedding(BaseEmbedding):
    """Gemini embedding provider via Google's native embeddings API."""

    DEFAULT_BASE_URL = "https://generativelanguage.googleapis.com/v1beta"

    def __init__(
        self,
        settings: Any,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        self.model = settings.embedding.model
        self.dimensions = getattr(settings.embedding, "dimensions", None)
        self.api_key = (
            api_key
            or getattr(settings.embedding, "api_key", None)
            or os.environ.get("GEMINI_API_KEY")
        )
        if not self.api_key:
            raise ValueError(
                "Gemini API key not provided. Set in settings.yaml (embedding.api_key), "
                "GEMINI_API_KEY environment variable, or pass api_key parameter."
            )

        raw_base_url = base_url or getattr(settings.embedding, "base_url", None)
        self.base_url = self._normalize_base_url(raw_base_url or self.DEFAULT_BASE_URL)
        self._extra_config = kwargs

    @staticmethod
    def _normalize_base_url(base_url: str) -> str:
        normalized = base_url.rstrip("/")
        if normalized.endswith("/openai"):
            normalized = normalized[: -len("/openai")]
        return normalized

    def embed(
        self,
        texts: List[str],
        trace: Optional[Any] = None,
        **kwargs: Any,
    ) -> List[List[float]]:
        self.validate_texts(texts)

        requests = [self._build_request(text, kwargs) for text in texts]
        url = f"{self.base_url}/models/{self.model}:batchEmbedContents"
        headers = {
            "x-goog-api-key": self.api_key,
            "Content-Type": "application/json",
        }

        try:
            with httpx.Client(timeout=60.0) as client:
                response = client.post(url, json={"requests": requests}, headers=headers)
                response.raise_for_status()
        except httpx.HTTPStatusError as e:
            detail = e.response.text
            raise GeminiEmbeddingError(
                f"Gemini Embeddings API error (HTTP {e.response.status_code}): {detail}"
            ) from e
        except httpx.RequestError as e:
            raise GeminiEmbeddingError(
                f"Gemini Embeddings connection failed: {type(e).__name__}: {e}"
            ) from e

        try:
            data = response.json()
            embeddings = [item["values"] for item in data["embeddings"]]
        except (KeyError, TypeError, ValueError) as e:
            raise GeminiEmbeddingError(
                f"Failed to parse Gemini Embeddings API response: {e}"
            ) from e

        if len(embeddings) != len(texts):
            raise GeminiEmbeddingError(
                f"Output length mismatch: expected {len(texts)}, got {len(embeddings)}"
            )

        return embeddings

    def _build_request(self, text: str, kwargs: dict[str, Any]) -> dict[str, Any]:
        request: dict[str, Any] = {
            "model": f"models/{self.model}",
            "content": {"parts": [{"text": text}]},
        }

        dimensions = kwargs.get("dimensions", self.dimensions)
        if dimensions is not None:
            request["outputDimensionality"] = dimensions

        return request

    def get_dimension(self) -> Optional[int]:
        if self.dimensions is not None:
            return self.dimensions

        model_dimensions = {
            "gemini-embedding-001": 3072,
            "gemini-embedding-2": 3072,
        }
        return model_dimensions.get(self.model)
