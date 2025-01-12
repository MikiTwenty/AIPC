# aipc/retrieval/upload.py

import uuid
import logging
from typing import List, Dict, Optional

from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
from sentence_transformers import SentenceTransformer
from qdrant_client.http.models import Distance, VectorParams

from ..utils import BaseClass


class QdrantDB(BaseClass):
    """
    Handles interaction with the Qdrant database.
    """
    def __init__(
            self,
            collection_name: str = 'aipc',
            host: str = "localhost",
            port: int = 6333,
            logger: Optional[logging.Logger] = None
        ) -> None:
        """
        Initializes the Qdrant handler.\n
        ---
        ### Args:
        - `collection_name` (`str`): name of the Qdrant collection.
        - `host` (`str`): host of the Qdrant server.
        - `port` (`int`): port of the Qdrant server.
        """
        super().__init__(logger)
        self.collection_name = collection_name
        self.client = QdrantClient(host=host, port=port)

        self.model = SentenceTransformer('all-MiniLM-L12-v2')
        vector_size = self.model.get_sentence_embedding_dimension()
        vector_params = VectorParams(size=vector_size, distance=Distance.COSINE)

        self.client.recreate_collection(
            collection_name = collection_name,
            vectors_config = vector_params)

    def generate_vector(self, text: str) -> List[float]:
        """
        Generates an embedding vector for a given text.\n
        ---
        ### Args:
        - `text` (`str`): input text to generate a vector.\n
        ---
        ### Returns:
        - `List[float]`: generated vector.
        """
        return self.model.encode(text).tolist()

    def insert_data(
            self,
            data: List[Dict]
        ) -> None:
        self.info(f"Inserting {len(data)} records into collection '{self.collection_name}'")

        points = []
        for item in data:
            caption_vector = self.generate_vector(item["caption"])
            unique_id = str(uuid.uuid4())  # Generate a unique ID for each point
            point = PointStruct(
                id = unique_id,
                vector = caption_vector,
                payload = {
                    "path": item["path"],
                    "caption": item["caption"],
                    "exif": item.get("exif")
                }
            )
            points.append(point)

        batch_size = 100
        for i in range(0, len(points), batch_size):
            batch = points[i:i + batch_size]
            self.client.upsert(collection_name=self.collection_name, points=batch)

    def search(
            self,
            query: str,
            limit: int = 10
        ) -> List[Dict]:
        """
        Retrieves records matching a given caption.\n
        ---
        ### Args:
        - `caption` (`str`): caption to search for.\n
        ---
        ### Returns:
        - `List[Dict]`: list of matching records.
        """
        query_vector = self.generate_vector(query)
        results = self.client.search(
            collection_name = self.collection_name,
            query_vector = query_vector,
            limit = limit)
        return [result.payload for result in results]