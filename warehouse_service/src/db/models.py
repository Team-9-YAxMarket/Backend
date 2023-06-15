import uuid
from sqlalchemy import Column, Numeric, Text, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Table


class Base(DeclarativeBase):
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"


sku_cargotype_table = Table(
    "sku_cargotype",
    Base.metadata,
    Column("sku", Text, ForeignKey("sku_ware.sku"), primary_key=True),
    Column(
        "cargotype",
        Integer,
        ForeignKey("cargotype_ware.cargotype"),
        primary_key=True,
    ),
)


class SKU(Base):
    __tablename__ = "sku_ware"

    sku = Column(Text, unique=True)
    length = Column(Numeric(precision=5, scale=1))
    width = Column(Numeric(precision=5, scale=1))
    height = Column(Numeric(precision=5, scale=1))
    weight = Column(Numeric(precision=5, scale=1))
    count = Column(Integer)
    barcode = Column(Text)

    cargotypes = relationship(
        "Cargotype", secondary=sku_cargotype_table, back_populates="skus"
    )


class Cargotype(Base):
    __tablename__ = "cargotype_ware"

    cargotype = Column(Integer, unique=True)
    description = Column(Text)

    skus = relationship(
        "SKU", secondary=sku_cargotype_table, back_populates="cargotypes"
    )


class Carton(Base):
    __tablename__ = "carton_ware"

    carton_type = Column(Text)
    length = Column(Numeric(precision=5, scale=1))
    width = Column(Numeric(precision=5, scale=1))
    height = Column(Numeric(precision=5, scale=1))
    barcode = Column(Text)
    count = Column(Integer)
