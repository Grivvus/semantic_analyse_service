import weaviate
import weaviate.classes as wvc
from weaviate.client import WeaviateClient

from app.model import vectorize_one
from app.settings import settings


def connect_to_vec_db() -> WeaviateClient:
    client = weaviate.connect_to_local(host=settings.WEAVIATE_HOST)
    return client


def get_collection(collection_name: str):
    client = connect_to_vec_db()
    return client.collections.get(collection_name)


def find_closest_vectors(
    collection_to_search: str,
    vector: list[float] | str,
    limit: int = 5,
):
    if type(vector) is str:
        vector = vectorize_one(vector)
    client = connect_to_vec_db()
    collection = client.collections.get(collection_to_search)
    response = collection.query.near_vector(
        near_vector=vector,  limit=limit
    )
    client.close()
    print("found something")
    return response
