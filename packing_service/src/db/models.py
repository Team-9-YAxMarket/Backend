import enum
import uuid
from datetime import datetime
from typing import Any, List, Optional

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM, TEXT, UUID
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(AsyncAttrs, DeclarativeBase):
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

        return "{}({})".format(
            self.__class__.__name__,
            ", ".join(
                [
                    "{}={}".format(c, add_quotes(getattr(self, c)))
                    for c in mandatory_columns
                ]
            ),
        )


item_prompt_table = sa.Table(
    "item_prompt",
    Base.metadata,
    sa.Column("item_id", sa.ForeignKey("items.id"), primary_key=True),
    sa.Column("prompt_id", sa.ForeignKey("prompts.id"), primary_key=True),
)

selected_carton_table = sa.Table(
    "selected_carton",
    Base.metadata,
    sa.Column("carton_id", sa.ForeignKey("cartons.id"), primary_key=True),
    sa.Column("order_id", sa.ForeignKey("orders.id"), primary_key=True),
)


class Prompt(Base):
    __tablename__ = "prompts"

    prompt: Mapped[str] = mapped_column(TEXT, nullable=False)
    items: Mapped[Optional[List["Item"]]] = relationship(
        secondary=item_prompt_table,
        back_populates="prompts",
    )

    __table_args__ = (sa.UniqueConstraint(prompt, name="uc_prompt"),)


class Carton(Base):
    __tablename__ = "cartons"

    carton_type: Mapped[str] = mapped_column(TEXT, nullable=False)
    barcode: Mapped[str] = mapped_column(TEXT, nullable=False)
    selected_for: Mapped[List["Order"]] = relationship(
        back_populates="selected_carton", secondary=selected_carton_table
    )

    __table_args__ = (sa.UniqueConstraint(carton_type, name="uc_carton_type"),)


class Item(Base):
    class ItemStatus(str, enum.Enum):
        """Статус элемента заказа."""

        ADDED = "added"
        SCANNED = "scanned"
        FAULT = "fault"
        ABSENT = "absent"

    __tablename__ = "items"

    status: Mapped[ItemStatus] = mapped_column(
        ENUM(ItemStatus, name="item_status"), default=ItemStatus.ADDED
    )
    sku: Mapped[str] = mapped_column(TEXT, nullable=False)
    barcode: Mapped[str] = mapped_column(TEXT, nullable=False)
    img: Mapped[str]
    count: Mapped[int]
    prompts: Mapped[Optional[List[Prompt]]] = relationship(
        secondary=item_prompt_table, back_populates="items"
    )
    box_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True))
    order_id: Mapped[Optional[UUID]] = mapped_column(
        sa.ForeignKey("orders.id")
    )
    order: Mapped["Order"] = relationship(back_populates="items")

    __table_args__ = (
        sa.CheckConstraint("count > 0", name="check_count_positive"),
    )


class RecommendedCarton(Base):
    """Recommended carton (Order and Carton) association table."""

    __tablename__ = "recommended_carton"

    order_id: Mapped[UUID] = mapped_column(
        sa.ForeignKey("orders.id"), primary_key=True
    )
    carton_id: Mapped[UUID] = mapped_column(
        sa.ForeignKey("cartons.id"), primary_key=True
    )
    carton: Mapped["Carton"] = relationship()
    box_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False)


class Order(Base):
    class OrderStatus(str, enum.Enum):
        """Статус заказа."""

        IS_FORMING = "is_forming"
        IS_COLLECTING = "is_collecting"
        IS_READY = "is_ready"

    __tablename__ = "orders"

    create_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow(),
        onupdate=datetime.utcnow(),
        nullable=False,
    )
    status: Mapped[OrderStatus] = mapped_column(
        ENUM(OrderStatus, name="order_status"), default=OrderStatus.IS_FORMING
    )
    items: Mapped[List[Item]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )
    recommended_carton: Mapped[
        Optional[List[RecommendedCarton]]
    ] = relationship(cascade="all, delete-orphan")
    selected_carton: Mapped[List["Carton"]] = relationship(
        secondary=selected_carton_table, back_populates="selected_for"
    )


class Session(Base):
    class SessionStatus(str, enum.Enum):
        """Статус сессии."""

        OPENED = "opened"
        CLOSED_SUCCESS = "closed_success"
        CLOSED_PROBLEM = "closed_problem"

    __tablename__ = "sessions"

    create_at: Mapped[datetime] = mapped_column(
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
    status: Mapped[SessionStatus] = mapped_column(
        ENUM(SessionStatus, name="session_status"),
        default=SessionStatus.OPENED,
    )
    order_id: Mapped[UUID] = mapped_column(
        sa.ForeignKey("orders.id", ondelete="SET NULL")
    )
    order: Mapped[Order] = relationship()
