from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import VARCHAR
from .database import Base

class Notas(Base):

    __tablename__ = "notas"

    id = Column(Integer, primary_key=True, index=True)
    disciplina = Column(VARCHAR(200), ForeignKey("disciplinas.name", ondelete="CASCADE", onupdate="CASCADE"))
    titulo = Column(VARCHAR(200), unique=True, index=True)
    descricao = Column(VARCHAR(200))

    materia = relationship("Disciplinas", back_populates="anotacoes")

class Disciplinas(Base):

    __tablename__ = "disciplinas"

    id = Column(Integer, primary_key=True, index=True)
    name =  Column(VARCHAR(200), unique=True, index=True)
    prof_name = Column(VARCHAR(200), index=True)

    anotacoes = relationship("Notas", back_populates="materia", cascade="all, delete-orphan")
