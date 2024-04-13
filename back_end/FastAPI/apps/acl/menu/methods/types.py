from pydantic import BaseModel, Field


class AddMenuModel(BaseModel):
    code: str | None
    createTime: str
    level: int
    name: str
    updateTime: str
    id_: str = Field(..., alias='id')
