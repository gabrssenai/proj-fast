from sqlalchemy import Session, create_engine

from proj_fast.models import table_registry

engine = create_engine('sqlite:///database.db')

table_registry.metadata.create_all(engine)
# uv run python -c "import proj_fast.database"


def get_session():
    with Session(engine) as session:
        yield session
