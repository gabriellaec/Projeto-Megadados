from typing import Optional
from fastapi import FastAPI, status, Form, Request, HTTPException
from fastapi.param_functions import Path
from pydantic import BaseModel, Field
from typing import List, Dict
from starlette.responses import RedirectResponse
from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


tags_metadata = [
    {
        "name": "disciplina",
        "description": "disciplinas que está cursando. Incluem nome, nome do professor, anotações e notas",
    },
    {
        "name": "notas",
        "description": "Conjunto de notas de cada matéria.",
    },
]

description = """
    Microsserviço de controle de notas para um App para gerenciar disciplinas 🚀
    Permite:
       - Criar disciplinas e notas
       - Consultar informações de cada disciplina
       - Alterar disciplinas e notas
       - Deletar disciplinas e notas
    

    Alunos: Gabriella Cukier e Manuel Castanares
"""


app = FastAPI(
    title="Minhas Disciplinas",
    description=description,
    version="0.0.1",
    openapi_tags=tags_metadata,
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#---------------------------------------------------#
#    	             Disciplinas    	            #
#---------------------------------------------------#
#####################################################
# • O usuário pode criar uma disciplina
#####################################################
@app.post("/disciplina/",  
status_code=status.HTTP_201_CREATED,
summary="Adicionar disciplina",
response_description="Adicionando disciplina",
response_model=schemas.Disciplina,
tags=["disciplina"]
)
def create_disciplina(disciplina: schemas.DisciplinaCreate, db: Session = Depends(get_db)):
    db_disciplina = crud.get_disciplina_by_name(db, nome=disciplina.name)
    if db_disciplina:
        raise HTTPException(status_code=400, detail="Disciplina já existe!")
    return crud.create_disciplina(db=db, disciplina=disciplina)


######################################################
# • O usuário pode listar os nomes de suas disciplinas
######################################################
@app.get("/disciplina/",
status_code=status.HTTP_200_OK,
summary="Listar os nomes das disciplinas",
response_description="Listando as disciplinas",
response_model=List[schemas.Disciplina],
tags=["disciplina"]
)

def get_disciplinas(db: Session = Depends(get_db)):
    """
     Lê todos os nomes das disciplinas existentes
    """
    disciplinas = crud.get_disciplinas(db)
    return disciplinas




##################################################################################
#U • O usuário pode modificar as informações de uma disciplina INCLUINDO seu nome
##################################################################################
@app.put("/disciplina/", 
status_code=status.HTTP_200_OK,
summary="Atualizar disciplina",
response_description="Atualizando disciplina",
response_model=schemas.Disciplina,
tags=["disciplina"]
)
async def update(
    nome_disciplina: str, infos: schemas.DisciplinaUpdate, db: Session = Depends(get_db)    
    ):
    """
    Atualiza as informações de uma determinada disciplina
    - **nome_disciplina**: A disciplina que será alterada
    - **novo_nome_disciplina**: Novo nome que a disciplina receberá
    - **nome_prof**: Novo nome do professor que se deseja alterar
    """
  
    db_disciplina = crud.get_disciplina_by_name(db, nome=nome_disciplina)
    if db_disciplina is None:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada!")
    return crud.update_disciplina(db, infos, nome=nome_disciplina)


##############################################
### • O usuário pode deletar uma disciplina
##############################################
@app.delete("/disciplina/",
status_code=status.HTTP_200_OK,
summary="Deletar disciplina",
response_description="Deletando disciplina",
tags=["disciplina"]
)
def delete_disciplina(
    nome_disciplina: str, db: Session = Depends(get_db)    
    ):
    """
    Deleta uma disciplina
    - **nome_disciplina**: Nome da disciplina que será deletada
    """
    db_disciplina = crud.get_disciplina_by_name(db, nome=nome_disciplina)
    if db_disciplina is None:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada!")

    return crud.delete_disciplina(db, nome=nome_disciplina)


#---------------------------------------------------#
#    	                 Notas    	                #
#---------------------------------------------------#
#######################################################
#C • O usuário pode adicionar uma nota a uma disciplina
#######################################################
@app.post("/disciplina/{nome_disciplina}/notas",  
status_code=status.HTTP_201_CREATED,
summary="Adicionar Nota",
response_description="Adicionando nota",
response_model=schemas.Nota,
tags=["notas"]
)
def create_nota(
    nome_disciplina: str, nota: schemas.NotaCreate, db: Session = Depends(get_db)
):
    """
    Cria uma nota com todos os atributos
    - **nome_disciplina**: nome da disciplina com a nova nota
    - **titulo**: titulo da nota 
    - **nota**: Nota a ser adicionada
    """

    db_disciplina = crud.get_disciplina_by_name(db, nome=nome_disciplina)
    if db_disciplina is None:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada!")


    query = crud.create_nota(db=db, nota=nota, disciplina=nome_disciplina)
    if query is None:
        raise HTTPException(status_code=404, detail="Já existe uma nota com esse nome nesta disciplina!")
   
    return query



#####################################################
#R • O usuário pode listar as notas de uma disciplina
#####################################################
@app.get("/disciplina/{nome_disciplina}/notas",
status_code=status.HTTP_200_OK,
summary="Listar notas de uma disciplina",
response_description="Listando as notas",
response_model=schemas.Nota,
tags=["notas"]
)
def get_nota_by_disciplina(nome_disciplina: str, db: Session = Depends(get_db)):
    """
     Lê todas as notas de uma disciplina
    - **nome_disciplina**: Nome da disciplina em que estão as notas
    """

    db_disciplina = crud.get_disciplina_by_name(db, nome=nome_disciplina)
    if db_disciplina is None:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada!")

    db_disciplina = crud.get_nota_by_disciplina(db, nome=nome_disciplina)
    if db_disciplina is None:
        raise HTTPException(status_code=404, detail="Você não tem notas para esta disciplina!")

    return db_disciplina



##########################################################
#U • O usuário pode modificar uma nota de uma disciplina
##########################################################
@app.patch("/disciplina/{nome_disciplina}/notas", 
status_code=status.HTTP_200_OK,
summary="Atualizar nota",
response_description="Atualizando nota",
response_model=schemas.Nota,
tags=["notas"]
)
async def update_nota(
    titulo: str, nome_disciplina: str, infos: schemas.NotaUpdate, db: Session = Depends(get_db)    
    ):
    """
    Atualiza uma nota de determinada matéria
    - **nome_disciplina**: A disciplina cuja nota vai ser alterada
    - **nome_titulo**: O título da nota a ser alterada
    - **nova_nota**: A nova nota a ser salva
    """
    db_disciplina = crud.get_nota_by_disciplina(db, nome=nome_disciplina)
    if db_disciplina is None:
        raise HTTPException(status_code=404, detail="Nota não encontrada!")
    return update_nota(db, infos, titulo, nome_disciplina)


#######################################
#D • O usuário pode deletar uma nota
#######################################
@app.delete("/disciplina/{nome_disciplina}/notas",
status_code=status.HTTP_200_OK,
summary="Deletar nota",
response_description="Deletando nota",
response_model=schemas.Nota,
tags=["notas"]
)
def delete_nota(
    titulo: str, nome_disciplina: str, db: Session = Depends(get_db)    
    ):
    """
    Deleta uma nota de determinada matéria
    - **nome_disciplina**: A disciplina em que a nota a ser deletada está
    - **nome_titulo**: O título cuja nota se deseja deletar
    """
    db_disciplina = crud.get_nota_by_disciplina(db, nome=nome_disciplina)
    if db_disciplina is None:
        raise HTTPException(status_code=404, detail="Nota não encontrada!")
    return crud.delete_nota(db, titulo=titulo, disciplina=nome_disciplina)
