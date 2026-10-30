# Data Model & Schemas

## 1. Database Schema (PostgreSQL / Supabase)

We will use a single primary table for the MVP: `compliance_events`. 

### Table: `compliance_events`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID | Primary Key, Default: `gen_random_uuid()` | Unique identifier for the event. |
| `source_url` | TEXT | UNIQUE, NOT NULL | The original URL of the article/regulation. Used for deduplication. |
| `title` | TEXT | NOT NULL | The headline or title of the regulation/event. |
| `raw_text` | TEXT | | The original ingested text (for audit/fallback). |
| `jurisdiction` | TEXT | NOT NULL | E.g., "Global", "EU", "US", "UK", "Estonia". |
| `status` | TEXT | NOT NULL | Enum: 'Proposed', 'In Force', 'Enforcement', 'Guidance'. |
| `effective_date` | DATE | Nullable | The date the regulation takes effect (if applicable). |
| `relevance_score`| INTEGER | CHECK (1 <= relevance_score <= 10) | AI-assigned score based on severity and scope. |
| `recommended_action`| TEXT | NOT NULL | AI-generated next step for a compliance officer. |
| `summary` | TEXT | NOT NULL | AI-generated 2-sentence summary. |
| `created_at` | TIMESTAMP | Default: `NOW()` | When the record was ingested. |

## 2. Python Pydantic Models (`src/models.py`)

These models enforce strict typing. If the LLM tries to return a string for the `relevance_score`, Pydantic will throw a validation error, preventing bad data from entering the database.

```python
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