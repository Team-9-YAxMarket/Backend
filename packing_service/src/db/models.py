import uuid
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import BYTEA, TEXT, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
    )

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(TEXT)

    def __repr__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id={self.id}, username={self.username})"
        )


class Session(Base):
    __tablename__ = "sessions"

    start_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow(),
        onupdate=datetime.utcnow(),
        nullable=False,
    )
    end_at: Mapped[datetime] = mapped_column(
        nullable=True,
    )
    ...
