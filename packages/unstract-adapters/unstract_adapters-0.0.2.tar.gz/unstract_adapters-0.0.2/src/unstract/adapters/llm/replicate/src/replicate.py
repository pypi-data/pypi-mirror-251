import os
from typing import Any, Optional

from llama_index.llms.llm import LLM
from llama_index.llms.replicate import Replicate
from unstract.adapters.llm.llm_adapter import LLMAdapter


class Constants:
    MODEL = "model"
    API_KEY = "api_key"
    IMAGE = "image"
    ADAPTER_NAME = "adapter_name"


class ReplicateLLM(LLMAdapter):
    def __init__(self, settings: dict[str, Any]):
        super().__init__("Replicate")
        self.config = settings

    @staticmethod
    def get_id() -> str:
        return "replicate|2715ce84-05af-4ab4-b8e9-67ac3211b81e"

    @staticmethod
    def get_name() -> str:
        return "Replicate"

    @staticmethod
    def get_description() -> str:
        return "Replicate LLM"

    @staticmethod
    def get_icon() -> str:
        return (
            "https://storage.googleapis.com/pandora-static/"
            "adapter-icons/Replicate.png"
        )

    @staticmethod
    def get_json_schema() -> str:
        f = open(f"{os.path.dirname(__file__)}/static/json_schema.json")
        schema = f.read()
        f.close()
        return schema

    @staticmethod
    def can_write() -> bool:
        return True

    @staticmethod
    def can_read() -> bool:
        return True

    def get_llm_instance(self) -> Optional[LLM]:
        # Adding this if-else to work-around Repilcate library's
        # expectation of image being set to "".
        # If not, errors out
        if self.config.get(Constants.IMAGE) is not None:
            llm = Replicate(
                model=str(self.config.get(Constants.MODEL)),
                image=str(self.config.get(Constants.IMAGE)),
                prompt_key=str(self.config.get(Constants.API_KEY)),
                temperature=0,
            )
        else:
            llm = Replicate(
                model=str(self.config.get(Constants.MODEL)),
                prompt_key=str(self.config.get(Constants.API_KEY)),
                temperature=0,
            )
        return llm
