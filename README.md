# Megadados-Projeto

## Conexão com o banco de dados:
Para conectar com o banco de dados, completar o arquivo secrets.py com seu usuário e senha do MySQL, de acordo com o template indicado

ATENÇÃO: O arquivo secrets.py deste repositório é apenas um template

ATENÇÃO2: Nunca divulgue as credenciais do banco de dados em um repositório

## Bibliotecas necessárias
pip install fastapi

pip install "uvicorn[standard]"

pip install sqlalchemy_utils


## Rodando o projeto:
uvicorn Proj1.main:app --reload
