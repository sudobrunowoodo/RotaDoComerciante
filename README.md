# Rota do Comerciante — Backend

API/servidor web em Flask para cadastro de feirantes, produtos e localizações.

## Requisitos

- **Python 3.10 ou superior** (testado com 3.11, 3.13 e 3.14)
- **pip** (já vem com o Python)
- **Conexão com a internet** (o cadastro consulta a BrasilAPI para validar o CNPJ)

O banco de dados é SQLite, que já vem com o Python. Não é preciso instalar nada além disso.

## Dependências

| Pacote | Para que serve |
|---|---|
| `Flask` | Framework web (já inclui o Jinja2, usado nos templates) |
| `Flask-SQLAlchemy` | ORM e conexão com o banco SQLite |
| `Flask-Login` | Controle de login e sessão |
| `bcrypt` | Hash de senhas |
| `requests` | Consulta de CNPJ na BrasilAPI |

## Instalação

Na pasta `backend`, crie um ambiente virtual e instale as dependências.

**Windows (PowerShell ou CMD):**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

```bash
pip install Flask Flask-SQLAlchemy Flask-Login bcrypt requests
```

## Estrutura de pastas esperada

O `backend` busca templates em duas pastas: `backend/templates` e `../frontend`.
Por isso, a pasta `frontend` precisa ficar **ao lado** do `backend`:

```
RotaDoComerciante/
├── backend/
│   ├── main.py              # ponto de entrada
│   ├── config.py            # app, Flask-Login, banco e loader de templates
│   ├── validators.py        # validações de produto e localização
│   ├── db.py                # instância do SQLAlchemy
│   ├── models.py            # tabelas (Feirantes, Perfil_feirantes, Produtos, Localizacao)
│   ├── utils.py             # verificar_cnpj (BrasilAPI)
│   ├── routes/
│   │   ├── feirantes.py     # login, registro, edição de feirantes
│   │   ├── produtos.py      # CRUD de produtos
│   │   └── localizacoes.py  # CRUD de localizações
│   ├── templates/
│   └── requirements.txt
└── frontend/                # contém, por exemplo, o registrar.html
```

## Como rodar

Com o ambiente virtual ativado, dentro da pasta `backend`:

```bash
python main.py
```

O servidor sobe em `http://127.0.0.1:5000`. As tabelas são criadas
automaticamente na primeira execução (`db.create_all()`), e o arquivo
`dados.db` é gerado pelo Flask-SQLAlchemy (normalmente dentro da pasta `instance/`).

## Rotas principais

| Rota | Descrição |
|---|---|
| `/registrar` | Cadastro de feirante (valida o CNPJ na BrasilAPI) |
| `/login`, `/logout` | Autenticação |
| `/` | Home (exige login) |
| `/produtos` | Lista, cadastra, edita e remove produtos |
| `/localizacoes` | Lista, cadastra, edita e remove a localização da barraca |

## Problemas comuns

- **`TemplateNotFound: registrar.html`**: o arquivo não está em `backend/templates` nem em `../frontend`. Confira se a pasta `frontend` está ao lado do `backend`.
- **Erro ao instalar o `bcrypt`**: atualize o pip com `python -m pip install --upgrade pip` e tente de novo.
- **CNPJ sempre "inativo"**: sem internet, ou a BrasilAPI está fora do ar, o cadastro cai no status `inativo`.
