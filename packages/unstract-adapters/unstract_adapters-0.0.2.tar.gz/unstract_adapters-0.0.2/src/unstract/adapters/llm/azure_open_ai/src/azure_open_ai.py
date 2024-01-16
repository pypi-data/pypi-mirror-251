import os
from typing import Any, Optional

from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.llms.llm import LLM
from unstract.adapters.llm.llm_adapter import LLMAdapter


class Constants:
    MODEL = "model"
    ENGINE = "engine"
    API_KEY = "api_key"
    API_VERSION = "api_version"
    MAX_RETIRES = "max_retries"
    ADAPTER_NAME = "adapter_name"
    ADAZURE_ENDPONT = "azure_endpoint"


class AzureOpenAILLM(LLMAdapter):
    def __init__(self, settings: dict[str, Any]):
        super().__init__("AzureOpenAI")
        self.config = settings

    @staticmethod
    def get_id() -> str:
        return "azureopenai|592d84b9-fe03-4102-a17e-6b391f32850b"

    @staticmethod
    def get_name() -> str:
        return "AzureOpenAI"

    @staticmethod
    def get_description() -> str:
        return "AzureOpenAI LLM"

    @staticmethod
    def get_icon() -> str:
        return (
            "https://storage.googleapis.com/pandora-static/"
            "adapter-icons/AzureopenAI.png"
        )

    @staticmethod
    def get_json_schema() -> str:
        f = open(f"{os.path.dirname(__file__)}/static/json_schema.json")
        schema = f.read()
        f.close()
        return schema

    def get_llm_instance(self) -> Optional[LLM]:
        llm = AzureOpenAI(
            model=str(self.config.get(Constants.MODEL)),
            deployment_name=str(self.config.get(Constants.ENGINE)),
            engine=str(self.config.get(Constants.ENGINE)),
            api_key=str(self.config.get(Constants.API_KEY)),
            api_version=str(self.config.get(Constants.API_VERSION)),
            azure_endpoint=str(self.config.get(Constants.ADAZURE_ENDPONT)),
            api_type="azure",
            temperature=0,
        )
        return llm
