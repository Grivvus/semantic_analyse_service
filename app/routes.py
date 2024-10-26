from typing import Annotated

from fastapi import APIRouter, Body

from app.logic import (
    find_closest_vectors,
    transform_data, transform_verbal_data,
    transform_query, guess_category
)
from app.model import vectorize_one
from app.pydantic_models import AnalyzeResponse, VerbalAnalyzeResponse

router = APIRouter()


@router.post("/analyze")
def analyze(query: Annotated[str, Body()]) -> list[AnalyzeResponse]:
    """do what needs to be done"""
    query = transform_query(query)
    vector = vectorize_one(query)
    closest_vectors = find_closest_vectors("Issue", vector)
    transformed = transform_data(closest_vectors)
    return transformed


@router.post("/verbal_analyze")
def verbal_analyze(
    query: Annotated[str, Body()]
) -> list[VerbalAnalyzeResponse]:
    """analyze + some extra data to easier testing"""
    query = transform_query(query)
    vector = vectorize_one(query)
    closest_vectors = find_closest_vectors("Issue", vector)
    transformed = transform_verbal_data(closest_vectors)
    return transformed


@router.post("/rocognize_category")
def recognize_category(query: Annotated[str | None, Body()]) -> str | None:
    """
    it's more mock than a real service,
    but sometimes it works
    """
    return guess_category(query)
