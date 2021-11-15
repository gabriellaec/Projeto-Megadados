# Megadados-Projeto

## Conexão com o banco de dados:
Para conectar com o banco de dados, completar o arquivo secrets.py com seu usuário e senha do MySQL, de acordo com o template indicado

ATENÇÃO: O arquivo secrets.py deste repositório é apenas um template

ATENÇÃO2: Nunca divulgue as credenciais do banco de dados em um repositório

## Bibliotecas necessárias
pip install fastapi

pip install "uvicorn[standard]"

pip install sqlalchemy_utils

pip install pymysql

## Rodando o projeto:
uvicorn Proj1.main:app --reload

Entrar no site da documentação
http://127.0.0.1:8000/docs#/

Preencher os parâmetros para testar os métodos CRUD, conforme descrito nas instruções (se o valor for opcional, tirar a chave e o valor do dicionário JSON)
