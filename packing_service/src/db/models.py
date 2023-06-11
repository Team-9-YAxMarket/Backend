import enum
import uuid
from datetime import datetime
from typing import Any, List, Optional

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import TEXT, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
    )

    def __repr__(self):
        def add_quotes(value: Any):
            """Add quotes to strings."""
            if isinstance(value, str):
                return f'"{value}"'
            if isinstance(value, list):
                return [add_quotes(i) for i in value]
            if isinstance(value, dict):
                return {add_quotes(k): add_quotes(v) for k, v in value.items()}
            return value

        mandatory_columns = [
            c.name
            for c in self.__class__.__table__.columns
            if c.primary_key or not c.nullable
        ]
        mandatory_columns.sort()

        return "{}({})".format(
            self.__class__.__name__,
            ", ".join(
                [
                    "{}={}".format(c, add_quotes(getattr(self, c)))
                    for c in mandatory_columns
                ]
            ),
        )


class SKU(Base):
    __tablename__ = "skus"

    sku: Mapped[str] = mapped_column(TEXT, nullable=False)
    barcode: Mapped[str] = mapped_column(TEXT, nullable=False)


class Prompt(Base):
    __tablename__ = "prompts"

    prompt: Mapped[str] = mapped_column(TEXT, nullable=False)


class Carton(Base):
    __tablename__ = "cartons"

    carton_type: Mapped[str] = mapped_column(TEXT, nullable=False)
    barcode: Mapped[str] = mapped_column(TEXT, nullable=False)


class ItemPrompt(Base):
    """Item and Prompt association table."""

    __tablename__ = "item_prompt"

    item: Mapped[UUID] = mapped_column(
        ForeignKey("items.id"), primary_key=True
    )
    prompt: Mapped[UUID] = mapped_column(
        ForeignKey("prompts.id"), primary_key=True
    )


class Item(Base):
    class Status(str, enum.Enum):
        """Статус элемента заказа."""

        ADDED = "added"
        SCANNED = "scanned"
        FAULT = "fault"
        ABSENT = "absent"

    __tablename__ = "items"

    status: Mapped[Status]
    sku_id: Mapped[UUID] = mapped_column(ForeignKey("skus.id"))
    sku: Mapped[SKU] = relationship()
    prompts: Mapped[Optional[List[ItemPrompt]]] = relationship()
    # recommended_carton: Mapped


class Order(Base):
    class Status(str, enum.Enum):
        """Статус заказа."""

        IS_FORMING = "is_forming"
        IS_COLLECTING = "is_collecting"
        IS_READY = "is_ready"

    __tablename__ = "orders"

    status: Mapped[Status]
    session_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("sessions.id")
    )
    session: Mapped[Optional["Session"]] = relationship(back_populates="order")
    # items: Mapped
    # recommended_carton: Mapped
    # selected_carton: Mapped


class Session(Base):
    class Status(str, enum.Enum):
        """Статус сессии."""

        OPENED = "started"
        CLOSED_SUCCESS = "closed_success"
        CLOSED_PROBLEM = "closed_problem"

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
    end_at: Mapped[datetime] = mapped_column(nullable=True)
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    status: Mapped[Status]
    order: Mapped[Order] = relationship(back_populates="session")
