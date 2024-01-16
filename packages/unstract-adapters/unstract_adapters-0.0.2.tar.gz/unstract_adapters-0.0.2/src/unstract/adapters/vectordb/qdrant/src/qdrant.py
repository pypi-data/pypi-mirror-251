import os
from typing import Any, Optional

from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.vector_stores.types import BasePydanticVectorStore
from qdrant_client import QdrantClient
from unstract.adapters.vectordb.vectordb_adapter import VectorDBAdapter


class Constants:
    URL = "url"
    API_KEY = "api_key"


class Qdrant(VectorDBAdapter):
    def __init__(self, settings: dict[str, Any]):
        super().__init__("Qdrant")
        self.config = settings

    @staticmethod
    def get_id() -> str:
        return "qdrant|41f64fda-2e4c-4365-89fd-9ce91bee74d0"

    @staticmethod
    def get_name() -> str:
        return "Qdrant"

    @staticmethod
    def get_description() -> str:
        return "Qdrant LLM"

    @staticmethod
    def get_icon() -> str:
        return (
            "https://storage.googleapis.com/pandora-static/"
            "adapter-icons/qdrant.png"
        )

    @staticmethod
    def get_json_schema() -> str:
        f = open(f"{os.path.dirname(__file__)}/static/json_schema.json")
        schema = f.read()
        f.close()
        return schema

    def get_vector_db_instance(self) -> Optional[BasePydanticVectorStore]:
        url = str(self.config.get(Constants.URL))
        qdrant_client = QdrantClient(url=url)
        vector_db = QdrantVectorStore(
            collection_name="unstract_2",
            client=qdrant_client,
        )
        return vector_db
