import json
import os
from typing import Any, Optional

from llama_index.embeddings import OpenAIEmbedding
from llama_index.embeddings.base import BaseEmbedding
from unstract.adapters.embedding.embedding_adapter import EmbeddingAdapter


class Constants:
    MODEL = "model"
    API_KEY = "api_key"
    API_BASE = "api_base"
    API_VERSION = "api_version"
    MAX_RETIRES = "max_retries"
    ADAPTER_NAME = "adapter_name"
    EMBED_BATCH_SIZE = "embed_batch_size"
    MAX_RETIRES = "max_retries"
    TIMEOUT = "timeout"
    VECTOR_SIZE = "vector_size"


class OpenAI(EmbeddingAdapter):
    def __init__(self, settings: dict[str, Any]):
        super().__init__("OpenAI")
        self.config = settings
        self.json_credentials = json.loads(
            settings.get("json_credentials", "{}")
        )

    @staticmethod
    def get_id() -> str:
        return "openai|717a0b0e-3bbc-41dc-9f0c-5689437a1151"

    @staticmethod
    def get_name() -> str:
        return "OpenAI"

    @staticmethod
    def get_description() -> str:
        return "OpenAI LLM"

    @staticmethod
    def get_icon() -> str:
        return (
            "https://storage.googleapis.com/pandora-static/"
            "adapter-icons/OpenAI.png"
        )

    @staticmethod
    def get_json_schema() -> str:
        f = open(f"{os.path.dirname(__file__)}/static/json_schema.json")
        schema = f.read()
        f.close()
        return schema

    def get_embedding_instance(self) -> Optional[BaseEmbedding]:
        embedding = OpenAIEmbedding(
            model=str(self.config.get("model")),
            api_base=str(self.config.get("api_base")),
            api_key=str(self.config.get("api_key")),
            api_version=str(self.config.get("api_version")),
            api_type="openai",
        )
        return embedding
