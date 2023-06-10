import enum
import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import TEXT, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
    )

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"


class SKU(Base):
    __tablename__ = "skus"

    sku: Mapped[TEXT]
    barcode: Mapped[TEXT]


class Carton(Base):
    __tablename__ = "cartons"

    carton_type: Mapped[TEXT]
    barcode: Mapped[TEXT]


class Prompt(Base):
    __tablename__ = "prompts"

    prompt: Mapped[TEXT]


class Item(Base):
    class Status(str, enum.Enum):
        """Статус сессии."""

        ADDED = "added"
        SCANNED = "scanned"
        FAULTY = "faulty"
        ABSENT = "absent"

    __tablename__ = "items"

    status: Mapped[Status]
    sku_id: Mapped[UUID] = mapped_column(ForeignKey("skus.id"))
    sku: Mapped["SKU"] = relationship()
    prompts: Mapped[Optional[List["Prompt"]]]
    # recommended_carton: Mapped


class Order(Base):
    class Status(str, enum.Enum):
        """Статус сессии."""

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
