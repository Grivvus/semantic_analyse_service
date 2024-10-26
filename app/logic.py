import weaviate
import weaviate.classes as wvc
from weaviate.client import WeaviateClient
from weaviate.classes.query import MetadataQuery

from app.model import vectorize_one
# from app.settings import settings
from app.pydantic_models import AnalyzeResponse, VerbalAnalyzeResponse


def connect_to_vec_db() -> WeaviateClient:
    client = weaviate.connect_to_local(host="weaviate")
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
        near_vector=vector,  limit=limit,
        return_metadata=MetadataQuery(distance=True)
    )
    client.close()
    print("found something")
    return response


def transform_data(response) -> list[AnalyzeResponse]:
    """transform data, fetched from db to valid form before send to frontend"""
    res = []
    for obj in response.objects:
        d = {
            "issue_id": obj.properties["issue_id"],
            "percentage": int((1 - obj.metadata.distance) * 100),
        }
        if d["percentage"] > 70:
            curr_obj = AnalyzeResponse(**d)
            res.append(curr_obj)
    return res


def transform_verbal_data(response) -> list[VerbalAnalyzeResponse]:
    """
    transform verbal data, fetched from db to valid form
    before send to frontend
    """
    res = []
    for obj in response.objects:
        d = {
            "issue_id": obj.properties["issue_id"],
            "percentage": int((1 - obj.metadata.distance) * 100),
            "issue_text": obj.properties["issue_text"],
            "issue_answer": obj.properties["solution"],
        }
        if d["percentage"] > 70:
            curr_obj = VerbalAnalyzeResponse(**d)
            res.append(curr_obj)
    return res


def transform_query(query: str) -> str:
    return (query.replace("I ", "").lower()
            .replace(".", "")
            .replace(",", "")
            .replace("?", "")
            .replace(" i ", " ")
            .replace(" you ", " ")
            .replace(" is ", " ")
            .replace(" are ", " ")
            .replace("i'm", "")
            .replace(" a ", " ")
            .strip()
            )


def guess_category(query: str) -> str | None:
    vec = vectorize_one(query)
    d = {}
    top_closest = find_closest_vectors("Issue", vec)
    for obj in top_closest.objects:
        if obj.properties["label"] in d.keys():
            d[obj.properties["label"]] += 1
        else:
            d[obj.properties["label"]] = 1
    for k in d.keys():
        if d[k] >= 4:
            return k
        else:
            None
