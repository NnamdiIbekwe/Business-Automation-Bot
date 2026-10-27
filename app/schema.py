from pydantic import BaseModel, Field

class Condition(BaseModel):
    field: str
    op: Literal["eq", "ne", "gt", "contains","lt", "gte", "lte"]
    value: Any

class Action(BaseModel):
    type: Literal["log", "webhook"]
    params: dict[str, Any] = {}

class WorkflowCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    event_type: str = Field(max_length=50)
    condition: Condition | None = None
    actions: list[Action] = Field(min_items=1)
    enabled: bool = True

class WorkflowOut(WorkflowCreate):
    id: int
    created_at: datetime

    model_config = (from_attributes=True,)

class workflowToggle(BaseModel):
    enabled: bool

class RunOut(BaseModel):
    id: int
    workflow_id: int
    status: str
    started_at: datetime | None = None
    completed_at: datetime | None = None
    result: dict | None = None

    model_config = (from_attributes=True,)

class EventCreate(BaseModel):
    event_type: str = Field(max_length=50)
    payload: dict = Field(default)

class EventOut(EventCreate):
    status: str
    model_config = (from_attribute)

