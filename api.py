import os
import shutil
import uuid
from datetime import datetime
from flask import Flask, request
import git
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

Base = declarative_base()

# Definindo o modelo do banco de dados para armazenar os resultados da análise
class GitAnalysisResult(Base):
    __tablename__ = 'git_analysis_results'

    id = Column(Integer, primary_key=True)
    author = Column(String)
    analyse_date = Column(DateTime)
    average_commits = Column(Float)
    repository_url = Column(String)
    repository_name = Column(String)


# Configura o banco de dados SQLite
engine = create_engine('sqlite:///git_analysis_results.db')
Base.metadata.create_all(engine)  # Cria a tabela apenas uma vez, durante a inicialização

# Configura o sessionmaker para gerenciar a sessão do banco
Session = sessionmaker(bind=engine)

@app.route('/analisador-git', methods=['GET'])
def git_analysis():
    try:
        # Recebe os parâmetros da requisição
        usuario = request.args.get('usuario')
        repositorio = request.args.get('repositorio')

        if not usuario or not repositorio:
            return {'error': 'Parâmetros "usuario" e "repositorio" são obrigatórios'}, 400

        repo_url = f'https://github.com/{usuario}/{repositorio}.git'

        # Cria um diretório único para cada requisição (evita concorrência)
        repo_dir = f'diretorio_local_repositorio_{uuid.uuid4()}'

        # Tenta clonar o repositório
        try:
            if os.path.exists(repo_dir):
                shutil.rmtree(repo_dir)
            repo = git.Repo.clone_from(repo_url, repo_dir)
        except Exception as e:
            return {'error': f'Erro ao clonar o repositório: {str(e)}'}, 400

        # Inicializa dicionários para armazenar os commits por autor e os dias por autor
        commits_por_desenvolvedor = {}
        dias_por_desenvolvedor = {}

        # Itera pelo histórico de commits uma única vez para contar commits e dias
        for commit in repo.iter_commits():
            autor = commit.author.name
            data_commit = commit.committed_datetime.date()

            # Contagem de commits
            if autor not in commits_por_desenvolvedor:
                commits_por_desenvolvedor[autor] = 0
            commits_por_desenvolvedor[autor] += 1

            # Contagem de dias
            if autor not in dias_por_desenvolvedor:
                dias_por_desenvolvedor[autor] = set()
            dias_por_desenvolvedor[autor].add(data_commit)

        # Inicializa o resultado da resposta
        response = ''

        # Armazena os resultados no banco de dados e prepara a resposta
        with Session() as session:
            for autor, commits in commits_por_desenvolvedor.items():
                dias = len(dias_por_desenvolvedor[autor])
                media_commits_por_dia = commits / dias
                response += f'{autor} realizou {commits} commits com uma média de {media_commits_por_dia:.2f} commits por dia.<br>'

                # Cria o objeto GitAnalysisResult
                result = GitAnalysisResult(
                    author=autor,
                    analyse_date=datetime.now(),
                    average_commits=media_commits_por_dia,
                    repository_url=repo_url,
                    repository_name=repositorio
                )
                session.add(result)
            session.commit()

        return response
    except Exception as e:
        return {'error': str(e)}, 400
    finally:
        # Remove o repositório clonado após a análise
        if os.path.exists(repo_dir):
            shutil.rmtree(repo_dir)


@app.route('/analisador-git/buscar', methods=['GET'])
def buscar_medias_de_commit():
    try:
        autor1 = request.args.get('autor1')
        autor2 = request.args.get('autor2')
        autor3 = request.args.get('autor3')

        autores = [autor1, autor2, autor3]
        autores = [autor for autor in autores if autor]  # Remove autores vazios

        if not autores:
            return {'error': 'Pelo menos um parâmetro de autor deve ser informado'}, 400

        # Consulta os resultados no banco de dados
        with Session() as session:
            resultados = {}
            for autor in autores:
                for registro in session.query(GitAnalysisResult).filter(GitAnalysisResult.author.ilike(f"%{autor}%")).all():
                    resultados[registro.author] = f'{registro.author} possui uma média de {registro.average_commits:.2f} commits por dia.'

            # Retorna os resultados sem duplicação
            return "<br>".join(resultados.values()) if resultados else 'Nenhum resultado encontrado para os autores informados.'
    except Exception as e:
        return {'error': str(e)}, 400


if __name__ == '__main__':
    app.run(debug=True)
