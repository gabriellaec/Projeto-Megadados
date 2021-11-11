from typing import List, Optional
from pydantic import BaseModel



class NotaBase(BaseModel):
    titulo: str  
    descricao: str 

class NotaCreate(NotaBase):
    pass

class Nota(NotaBase):
    id: int
    disciplina: str
    class Config:
        orm_mode = True



class DisciplinaBase(BaseModel):
    name: str
    prof_name: Optional[str]

class DisciplinaCreate(DisciplinaBase):
    pass

class Disciplina(DisciplinaBase):
    id: int
    class Config:
        orm_mode = True



class DisciplinaUpdate(BaseModel):
    name: Optional[str]
    prof_name: Optional[str]


class NotaUpdate(BaseModel):
    descricao: str
