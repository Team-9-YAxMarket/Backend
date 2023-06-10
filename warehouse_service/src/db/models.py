import uuid
from sqlalchemy import Column, Numeric
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import TEXT, UUID,INT
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
    __tablename__ = "sku_ware"

    sku: Mapped[TEXT]
    length: Column(Numeric(precision=5, scale=1))
    width: Column(Numeric(precision=5, scale=1))
    height: Column(Numeric(precision=5, scale=1))
    weight: Column(Numeric(precision=5, scale=1))
    barcode: Mapped[TEXT]

    sku_cargotypes = relationship("SkuCargotype", back_populates="sku")


class Cargotype(Base):
    __tablename__ = "cargotype_ware"
    cargotype: Mapped[INT]
    description: Mapped[TEXT]

    sku_cargotypes = relationship("SkuCargotype", back_populates="cargotype")


class Carton(Base):
    __tablename__ = "carton_ware"

    carton_type: Mapped[TEXT]
    length: Column(Numeric(precision=5, scale=1))
    width: Column(Numeric(precision=5, scale=1))
    height: Column(Numeric(precision=5, scale=1))
    barcode: Mapped[TEXT]


class SkuCargotype(Base):
    __tablename__ = "sku_cargo"
    sku_id: Mapped[UUID] = mapped_column(ForeignKey("sku_ware.id"))
    cartontype_id: Mapped[UUID] = mapped_column(ForeignKey("cargotype_ware.id"))

    sku = relationship("SKU", back_populates="sku_cargotypes")
    cargotype = relationship("Cargotype", back_populates="sku_cargotypes")


