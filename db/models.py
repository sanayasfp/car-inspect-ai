import dataclasses
from typing import Optional
from datetime import datetime as dt
from db.base_model import BaseModel
from db.field import Field


@dataclasses.dataclass
class TrainLogsModel(BaseModel):
    _table_name = "train_logs"

    name: str
    epochs: int
    model: str
    path: str
    completed: bool = Field(type=bool, default=False).set()
    id: Optional[int] = Field(type=int, primary_key=True, autoincrement=True).set()
    created_at: Optional[float] = Field(type=int, default=lambda: dt.now().timestamp()).set()
    resumed_from: Optional[int] = Field(type=int, foreign_key="id", foreign_table=_table_name).set()
