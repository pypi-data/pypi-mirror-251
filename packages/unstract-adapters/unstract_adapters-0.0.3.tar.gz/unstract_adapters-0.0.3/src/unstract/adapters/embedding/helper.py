from typing import Any


class EmbeddingConstants:
    DEFAULT_EMBED_BATCH_SIZE = 10
    EMBED_BATCH_SIZE = "embed_batch_size"


class EmbeddingHelper:
    @staticmethod
    def get_mebedding_batch_size(config: dict[str, Any]) -> int:
        if config.get(EmbeddingConstants.EMBED_BATCH_SIZE) is None:
            embedding_batch_size = EmbeddingConstants.DEFAULT_EMBED_BATCH_SIZE
        else:
            embedding_batch_size = int(
                config.get(
                    EmbeddingConstants.EMBED_BATCH_SIZE,
                    EmbeddingConstants.DEFAULT_EMBED_BATCH_SIZE,
                )
            )
        return embedding_batch_size
