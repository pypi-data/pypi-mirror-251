import json
import os
from typing import Any, Optional

from llama_index.embeddings.base import BaseEmbedding
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from unstract.adapters.embedding.embedding_adapter import EmbeddingAdapter


class Constants:
    ADAPTER_NAME = "adapter_name"
    MODEL = "model"
    TOKENIZER_NAME = "tokenizer_name"
    MAX_LENGTH = "max_length"
    NORMALIZE = "normalize"
    EMBED_BATCH_SIZE = "embed_batch_size"
    VECTOR_SIZE = "vector_size"


class HuggingFace(EmbeddingAdapter):
    def __init__(self, settings: dict[str, Any]):
        super().__init__("HuggingFace")
        self.config = settings
        self.json_credentials = json.loads(
            settings.get("json_credentials", "{}")
        )

    @staticmethod
    def get_id() -> str:
        return "huggingface|90ec9ec2-1768-4d69-8fb1-c88b95de5e5a"

    @staticmethod
    def get_name() -> str:
        return "HuggingFace"

    @staticmethod
    def get_description() -> str:
        return "HuggingFace LLM"

    @staticmethod
    def get_icon() -> str:
        return (
            "https://storage.googleapis.com/pandora-static/"
            "adapter-icons/huggingface.png"
        )

    @staticmethod
    def get_json_schema() -> str:
        f = open(f"{os.path.dirname(__file__)}/static/json_schema.json")
        schema = f.read()
        f.close()
        return schema

    def get_embedding_instance(self) -> Optional[BaseEmbedding]:
        embedding = HuggingFaceEmbedding(
            model_name=str(self.config.get(Constants.MODEL)),
            tokenizer_name=str(self.config.get(Constants.TOKENIZER_NAME)),
            normalize=bool(self.config.get(Constants.NORMALIZE)),
        )
        return embedding
