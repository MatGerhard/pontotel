# Desafio técnico PontoTel para vagas back-end
Esse repositório contém o código usado para avaliação de candidados a vagas de desenvolvedor(a) back-end.

O desafio consiste em melhorar o código aqui encontrado e resolver possíveis problemas.

## Objetivo do projeto
O objetivo do projeto é oferecer 2 rotas de uma API em que cada uma terá o seguinte comportamento:
- `/analisador-git?usuario=...&repositorio=...`: Realiza uma análise em um repositório público do GitHub onde será retornado a quantidade de commits por autor e a média de commits por dia trabalhado;
- `/analisador-git/buscar?autor1=...&autor2=...&autor3=...`:  Responsável por buscar análises de commits já realizadas anteriormente para os autores informados nos parâmetros autor1, autor2 e autor3. Pelo menos um dos parâmetros deve ser informado para obter um resultado.

## Critérios que serão avaliados

- Reorganização dos arquivos e pastas do projeto
- Normalizar o banco de dados
- Gerenciamento do diretório local usado para clonar o repositório
    - O código deve ser capaz de ser executado concorrentemente sem afetar os resultados de outros processos
    - O repositório deve ser descartado após a análise (pelo seu código ou pelo sistema operacional)
- Tratar possíveis erros externos e retornar uma resposta com o código 400
- Evitar loops desnecessários e otimizar execução do código
- Gerenciar corretamente sessões do banco de dados
- Gerenciar corretamente a criação das tabelas no banco de dados
    - Uso de migrations com o alembic para o versionamento da estrutura do banco
- Reaproveitar e reestruturar o código de forma clara e eficiente
- Otimizar uso do banco de dados e evitar consultas desnecessárias
- Criar testes unitários e/ou de integração para novas classes e funções
- Evitar que os testes falhem por dependências externas
- Atribuir tipos a classes, funções e variáveis
- BÔNUS: Criar um Dockerfile para a execução do projeto em um container

A conclusão de todos os critérios não é uma obrigação, porém quanto mais critérios forem concluídos, mais chances você terá de melhorar a sua avaliação.

Cada critério possui um peso diferente que seguirá a sua dificuldade para ser atingido.

### RESOLVA O DESAFIO SEM O USO DE NOVAS DEPENDÊNCIAS

# Como executar em sua máquina

## Servidor
- Garanta que a sua máquina possui o Python 3.9
- Faça a instalação do Poetry (https://python-poetry.org/docs/#installation)
- Em um terminal, navegue até a raiz desse projeto e execute o comando `poetry install`
- Entre no ambiente criado pelo poetry usando o comando `poetry shell`
- Execute o projeto digitando `python api.py`

## Testes
Para executar os testes basta escrever em um terminal na raiz do projeto: `pytest tests.py`
