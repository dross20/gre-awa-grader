from pydantic import BaseModel, Field
from typing import List
from typing_extensions import TypedDict

class Essay(BaseModel):
    prompt: str = Field(
        description="The prompt for the essay. If it's not explicitly stated, infer it from the content of the essay."
    )

    body: str = Field(
        description="The body of the essay written by the writer, not including the prompt."
    )

class EssayGrade(BaseModel):
    score: float = Field(
        description="The score for the analytical writing assessment section of the GRE"
    )

    rationale: str = Field(
        description="The reasoning, including strengths and weaknesses, for the score given"
    )

    improvement: str = Field(
        description="A few specific and descriptive ways that the writer could improve their essay"
    )

class GradeDocuments(BaseModel):
    binary_score: str = Field(
        description="Documents are relevant to the question, 'yes' or 'no'"
    )

class GraphState(TypedDict):
    essay: str = Field(
        description="The essay submitted by the user"
    )

    prompt: str = Field(
        description="The prompt for the essay"
    )

    body: str = Field(
        description="The body of the essay"
    )

    score: float = Field(
        description="The given score for the analytical writing assessment section of the GRE"
    )

    rationale: str = Field(
        description="The reasoning, including strengths and weaknesses, for the score given"
    )

    improvement: str = Field(
        description="A few specific and descriptive ways that the writer could improve their essay"
    )

    documents: List[str] = Field(
        description="The retrieved documents used as context to suggest improvements"
    )

    generations: str = Field(
        description="The final improvement generated with the assistance of documents from the vector store or the web"
    )