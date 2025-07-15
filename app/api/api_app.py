from pydantic import BaseModel

class AppBase(BaseModel):
    name: str
    route: str
    category: str
    status: int

class App(AppBase):
    id: int

    class Config:
        orm_mode = True
