from sqlalchemy.orm import Session
from . import models, schemas


def get_disciplinas(db: Session):
    return db.query(models.Disciplinas).all()


def get_disciplina_by_name(db: Session, nome: str):
    return db.query(models.Disciplinas).filter(models.Disciplinas.name == nome).first()

def get_id_by_name(db: Session, name: str):
    return db.query(models.Disciplinas).filter(models.Disciplinas.name == name).first().id

def check_notas_disciplina(db: Session, nome: str):
    id=get_id_by_name(db, nome)
    return db.query(models.Notas).filter(models.Notas.disciplina == id).all()

def get_nota_by_disciplina(db: Session, nome: str, titulo: str):
    id=get_id_by_name(db, nome)
    return db.query(models.Notas).filter(models.Notas.disciplina == id, models.Notas.titulo == titulo).first()


def create_disciplina(db: Session, disciplina: schemas.DisciplinaCreate):
    db_disciplina = models.Disciplinas(name=disciplina.name, prof_name=disciplina.prof_name)
    db.add(db_disciplina)
    db.commit()
    db.refresh(db_disciplina)
    return db_disciplina


def create_nota(db: Session, nota: schemas.NotaCreate, disciplina: str):
    id=get_id_by_name(db, disciplina)
    db_nota = models.Notas(disciplina=id, titulo=nota.titulo, descricao=nota.descricao)

    db_disciplina = db.query(models.Notas).filter( (models.Notas.disciplina == id), (models.Notas.titulo == nota.titulo)).first()

    if db_disciplina is None:
        db.add(db_nota)
        db.commit()
        db.refresh(db_nota)
        return db_nota
    return None


def delete_disciplina(db: Session, nome: str):
    deleted = db.query(models.Disciplinas).filter(models.Disciplinas.name == nome).delete()
    db.commit()
    if deleted:
        return f"{nome} deletada com sucesso!"
    else:
        return "Não foi possível deletar a disciplina"
    
def delete_nota(db: Session, titulo: str, disciplina: str):
    id=get_id_by_name(db, disciplina)
    deleted = db.query(models.Notas).filter((models.Notas.titulo == titulo), (models.Notas.disciplina == id)).delete()
    db.commit()
    if deleted:
        return f"{titulo} deletada com sucesso!"
    else:
        return "Não foi possível deletar a nota"

def update_disciplina(db: Session, infos: schemas.DisciplinaUpdate, nome: str):
    db_disciplina = db.query(models.Disciplinas).filter(models.Disciplinas.name == str(nome)).first()
    if infos.name is not None:
        if get_disciplina_by_name(db, infos.name) is None:
            db_disciplina.name = infos.name
        else:
            return None
            
    if infos.prof_name is not None:
        db_disciplina.prof_name = infos.prof_name 
    
    db.commit()
    # db.refresh(db_disciplina)

    return db_disciplina


def update_nota(db: Session, descricao: str, titulo: str, disciplina: str):
    id=get_id_by_name(db, disciplina)
    db_nota = db.query(models.Notas).filter((models.Notas.disciplina == id), (models.Notas.titulo == str(titulo))).first()
    db_nota.descricao = descricao
    db.commit()
    db.refresh(db_nota)
    return db_nota
