```
fastapi-project
├── alembic/
├── src
│   ├── auth
│   │   ├── __init__.py
│   │   ├── router.py
│   │   ├── schemas.py  # pydantic models
│   │   ├── models.py  # db models
│   │   ├── dependencies.py
│   │   ├── config.py  # local configs
│   │   └── service.py
│   ├── aws
│   │   ├── client.py  # client model for external service communication
│   │   ├── schemas.py
│   │   ├── config.py
│   │   ├── constants.py
│   │   ├── exceptions.py
│   │   └── utils.py
│   ├── posts
│   │   ├── __init__.py
│   │   ├── router.py
│   │   ├── schemas.py
│   │   ├── models.py
│   │   ├── dependencies.py
│   │   └── service.py
│   ├── __init__.py
│   ├── config.py  # global configs
│   ├── models.py  # global models
│   ├── exceptions.py  # global exceptions
│   ├── pagination.py  # global module e.g. pagination
│   ├── utils.py # helper functions
│   └── constants.py # constants
├── tests/
│   ├── auth
│   ├── aws
│   └── posts
├── templates/
│   └── index.html
├── requirements
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
├── .env
├── main.py
├── database.py  # db connection related stuff
├── .gitignore
├── logging.ini
└── alembic.ini
```

#### Create migrations directory
```python
alembic init migrations
```
alembic init <name_of_migrations_directory>

#### Edit alembic.ini file to point to our DB
```python
sqlalchemy.url = postgresql://postgres:postgres@localhost/fastapi_demo
```
sqlalchemy.url = "postgresql://user:password@host/db_name"

#### Edit migrations/env.py file to add your models and set metadata
```python
from src.auth.models import User
from src.blog.models import Blog
from database import Base
target_metadata = Base.metadata
```

**_NOTE_** : To **detect data_type and default value changes**, add these lines to run_migrations_offline() and run_migrations_online() **context.configure()** method in migrations/env.py file 
```python
compare_type=True,
compare_server_default=True
```

#### Create new migration script
```python
alembic revision --autogenerate -m "Create User and Blog Table"
```
It will create new script in alembic/versions directory


#### Apply migrations
```python
alembic upgrade +1
alembic downgrade -1
```