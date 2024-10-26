from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.post("/analyze")
def analyze(query: str) -> list[tuple[int, int]]:
    raise NotImplementedError
