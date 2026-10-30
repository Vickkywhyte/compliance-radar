from pydantic import BaseModel, Field, HttpUrl
from typing import Literal, Optional
from datetime import date


class ComplianceEvent(BaseModel):
    title: str = Field(description="The headline of the regulation or enforcement action.")
    source_url: HttpUrl = Field(description="The direct URL to the primary source.")
    jurisdiction: str = Field(description="The primary jurisdiction affected (e.g., Global, EU, US, UK).")
    status: Literal['Proposed', 'In Force', 'Enforcement', 'Guidance'] = Field(
        description="The current regulatory status."
    )
    effective_date: Optional[date] = Field(
        default=None,
        description="The date the rule takes effect. Null if not applicable."
    )
    relevance_score: int = Field(
        ge=1, le=10,
        description="1=Low impact/Niche, 10=Critical global AML change affecting all institutions."
    )
    summary: str = Field(
        description="A concise, 2-sentence summary of the event."
    )
    recommended_action: str = Field(
        description="A specific, actionable next step for a compliance officer."
    )
