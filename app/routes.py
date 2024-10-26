from typing import Annotated

from fastapi import APIRouter, HTTPException, Body

from app.logic import (
    connect_to_vec_db, find_closest_vectors,
    transform_data, transform_verbal_data,
    transform_query, guess_category
)
from app.model import vectorize_one
from app.pydantic_models import AnalyzeResponse, VerbalAnalyzeResponse

router = APIRouter()


@router.post("/analyze")
def analyze(query: Annotated[str, Body()]) -> list[AnalyzeResponse]:
    query = transform_query(query)
    vector = vectorize_one(query)
    closest_vectors = find_closest_vectors("Issue", vector)
    transformed = transform_data(closest_vectors)
    return transformed


@router.post("/verbal_analyze")
def verbal_analyze(
    query: Annotated[str, Body()]
) -> list[VerbalAnalyzeResponse]:
    query = transform_query(query)
    vector = vectorize_one(query)
    closest_vectors = find_closest_vectors("Issue", vector)
    transformed = transform_verbal_data(closest_vectors)
    return transformed


@router.post("/rocognize_category")
def recognize_category(query: Annotated[str | None, Body()]) -> str | None:
    return guess_category(query)
