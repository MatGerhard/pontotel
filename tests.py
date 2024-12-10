import os
import git
import pytest
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import api

@pytest.fixture(scope="module")
def flask_app():
    # Retorna a instância Flask definida no seu arquivo `api.py`
    app = api.app
    return app


@pytest.fixture(scope="module")
def db_session():
    # Cria uma nova sessão para cada teste
    engine = create_engine('sqlite:///git_analysis_results.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    # Limpa o banco de dados após os testes
    engine.execute('DELETE FROM git_analysis_results')


def test_git_analysis(flask_app, db_session):
    # Testa o endpoint /analisador-git
    with flask_app.test_request_context('/analisador-git?usuario=gitpython-developers&repositorio=gitdb'):
        result = api.git_analysis()
        assert 'Sebastian Thiel realizou 268 commits com uma média de 2.95 commits por dia.' in result

    # Testa o endpoint /analisador-git/buscar
    with flask_app.test_request_context('/analisador-git/buscar?autor1=Sebastian'):
        result = api.buscar_medias_de_commit()
        assert 'Sebastian Thiel possui uma média de 2.95 commits por dia.' in result


def test_git_analysis_no_repo(flask_app):
    # Testa o caso em que o repositório não existe
    with flask_app.test_request_context('/analisador-git?usuario=nonexistent-user&repositorio=nonexistent-repo'):
        result = api.git_analysis()
        assert 'Erro ao clonar o repositório' in result


def test_git_analysis_missing_params(flask_app):
    # Testa o caso em que faltam parâmetros obrigatórios
    with flask_app.test_request_context('/analisador-git?usuario=gitpython-developers'):
        result = api.git_analysis()
        assert 'Parâmetros "usuario" e "repositorio" são obrigatórios' in result


def test_git_analysis_empty_results(flask_app, db_session):
    # Testa o caso em que nenhum resultado é encontrado para o autor
    with flask_app.test_request_context('/analisador-git/buscar?autor1=nonexistent-author'):
        result = api.buscar_medias_de_commit()
        assert 'Nenhum resultado encontrado para os autores informados.' in result
