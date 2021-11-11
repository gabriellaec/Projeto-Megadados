from sqlalchemy.orm import Session
from . import models, schemas


def get_disciplinas(db: Session):
    return db.query(models.Disciplinas).all()


def get_disciplina_by_name(db: Session, nome: str):
    return db.query(models.Disciplinas).filter(models.Disciplinas.name == nome).first()


def get_nota_by_disciplina(db: Session, nome: str):
    return db.query(models.Notas).filter(models.Notas.disciplina == nome).first()


def create_disciplina(db: Session, disciplina: schemas.DisciplinaCreate):
    db_disciplina = models.Disciplinas(name=disciplina.name, prof_name=disciplina.prof_name)
    db.add(db_disciplina)
    db.commit()
    db.refresh(db_disciplina)
    return db_disciplina


def create_nota(db: Session, nota: schemas.NotaCreate, disciplina: str):
    db_nota = models.Notas(disciplina=disciplina, titulo=nota.titulo, descricao=nota.descricao)

    db_disciplina = db.query(models.Notas).filter( (models.Notas.disciplina == disciplina), (models.Notas.titulo == nota.titulo)).first()

    if db_disciplina is None:
        db.add(db_nota)
        db.commit()
        db.refresh(db_nota)
        return db_nota
    return None


def delete_disciplina(db: Session, nome: str):
    return db.query(models.Disciplinas).filter(models.Disciplinas.name == nome).delete()
    
def delete_nota(db: Session, titulo: str, disciplina: str):
    return db.query(models.Notas).filter((models.Notas.titulo == titulo), (models.Notas.disciplina == disciplina)).delete()
    

def update_disciplina(db: Session, infos: schemas.DisciplinaUpdate, nome: str):
    db_disciplina = db.query(models.Disciplinas).filter(models.Disciplinas.name == str(nome)).first()
    if infos.name is not None:
        db_disciplina.name = infos.name
    if infos.prof_name is not None:
        db_disciplina.prof_name = infos.prof_name
    db.commit()
    db.refresh(db_disciplina)
    return db_disciplina


def update_nota(db: Session, infos: schemas.NotaUpdate, titulo: str, disciplina: str):
    db_nota = db.query(models.Notas).filter((models.Notas.disciplina == str(disciplina)), (models.Notas.titulo == str(titulo))).first()
    db_nota.descricao = infos.descricao
    db.commit()
    db.refresh(db_nota)
    return db_nota
