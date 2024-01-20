from abc import ABC
from typing import Any, Optional, Union

from llama_index.vector_stores.types import BasePydanticVectorStore, VectorStore
from unstract.adapters.base import Adapter
from unstract.adapters.enums import AdapterTypes
from unstract.adapters.vectordb.constants import VectorDbConstants


class VectorDBAdapter(Adapter, ABC):
    def __init__(self, name: str):
        super().__init__(name)
        self.name = name

    @staticmethod
    def get_id() -> str:
        return ""

    @staticmethod
    def get_name() -> str:
        return ""

    @staticmethod
    def get_description() -> str:
        return ""

    @staticmethod
    def get_icon() -> str:
        return ""

    @staticmethod
    def get_json_schema() -> str:
        return ""

    @staticmethod
    def get_adapter_type() -> AdapterTypes:
        return AdapterTypes.VECTOR_DB

    def get_vector_db_instance(
        self, vector_db_config: dict[str, Any]
    ) -> Union[BasePydanticVectorStore, VectorStore, None]:
        return None

    @staticmethod
    def get_db_name(
        collection_name_prefix: Optional[str], embedding_type: Optional[str]
    ) -> str:
        """
        Notes:
            This function constructs the collection / db name to store the
            documents in the vector db.
            If user supplies this field in the config metadata then system
            would pick that and append it as prefix to embedding type.
            If this does not come as user setting, then system looks for it
            in the get_vector_db() argument and append it to embedding type
            If it is not there in both places then system appends
            "unstract_vector_db" as prefix to embedding type.
            If embedding type is not passed in get_vector_db() as arg,
            then system ignores appending that
        Args:
            collection_name_prefix (str): the prefix to be added. If this is
                    not passed in, then the default DEFAULT_VECTOR_DB_NAME
                    will be picked up for prefixing
            embedding_type (str): this will be suffixed. If this value is not
                    passed in, then only collection_name_prefix will be returned
                Eg. collection_name_prefix -> unstract_db
                    embedding_type -> open_ai
                    return value -> unstract_db_open_ai

                    collection_name_prefix -> No value
                    embedding_type -> No value
                    return value -> unstract_vector_db

        """
        if collection_name_prefix is None:
            collection_name_prefix = VectorDbConstants.DEFAULT_VECTOR_DB_NAME
        db_name: str = collection_name_prefix
        if embedding_type is not None:
            db_name = db_name + "_" + embedding_type
        return db_name
