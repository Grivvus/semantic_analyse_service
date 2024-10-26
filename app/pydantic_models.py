from pydantic import BaseModel


class AnalyzeResponse(BaseModel):
    issue_id: int
    percentage: int


class VerbalAnalyzeResponse(BaseModel):
    issue_id: int
    percentage: int
    issue_text: str
    issue_answer: str
