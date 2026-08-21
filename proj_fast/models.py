from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_as_dataclass, mapped_column, registry

table_registry = registry()


@mapped_as_dataclass(table_registry)
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        init=False,
        primary_key=True,
    )
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now(),
    )

@mapped_as_dataclass(table_registry)
class Interest:
    __tablename__ = "interests"

    id: Mapped[int] = mapped_column(
        init=False,
        primary_key=True,
    )
    nome: Mapped[str]
    email: Mapped[str]
    cidade: Mapped[str]
    veiculo_id: Mapped[int]
    veiculo_modelo: Mapped[str]

    status: Mapped[str] = mapped_column(
        default="novo",
    )

    created_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now(),
    )