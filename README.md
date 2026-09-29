# Gerenciador de Atividades — Flask

Aplicação web acadêmica para cadastro e gerenciamento de atividades usando Python, Flask, SQLite, HTML e CSS.

## Funcionalidades
- Cadastrar, editar, concluir e excluir atividades.
- Data de entrega, prioridade e status.
- Filtros e contadores.
- Organização modular e testes básicos.

## Estrutura
app/ (rotas, modelos, templates e CSS), database/, tests/, config.py, requirements.txt e run.py.

## Execução
`pip install -r requirements.txt`
`python run.py`

Arquitetura: Usuário → Interface → Rotas Flask → Modelos → SQLite → Interface.
