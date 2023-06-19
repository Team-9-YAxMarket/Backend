"""initial migration

Revision ID: 7a6ac8331c5a
Revises: 
Create Date: 2023-06-17 01:00:53.517728

"""
import uuid
from csv import DictReader

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a6ac8331c5a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    cargotype_ware = op.create_table('cargotype_ware',
                                     sa.Column('cargotype', sa.Integer(),
                                               unique=True),
                                     sa.Column('description', sa.Text(),
                                               nullable=True),
                                     sa.Column('id', sa.UUID(),
                                               primary_key=True),
                                     sa.PrimaryKeyConstraint('id'),
                                     sa.UniqueConstraint('cargotype')
                                     )

    file_path = './src/data/cargotype_info.csv'
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = DictReader(file)
        data_list = [
            {
                'cargotype': int(row['cargotype']),
                'description': row['description'],
                'id': uuid.uuid4() if 'id' not in row else uuid.UUID(
                    row['id'])
            }
            for row in reader
        ]
        op.bulk_insert(cargotype_ware, data_list)
    carton_ware = op.create_table('carton_ware',
                                  sa.Column('carton_type', sa.Text(),
                                            nullable=True),
                                  sa.Column('length',
                                            sa.Numeric(precision=5, scale=1),
                                            nullable=True),
                                  sa.Column('width',
                                            sa.Numeric(precision=5, scale=1),
                                            nullable=True),
                                  sa.Column('height',
                                            sa.Numeric(precision=5, scale=1),
                                            nullable=True),
                                  sa.Column('barcode', sa.Text(),
                                            nullable=True),
                                  sa.Column('count', sa.Integer(),
                                            nullable=True),
                                  sa.Column('id', sa.UUID(), primary_key=True),
                                  sa.PrimaryKeyConstraint('id')
                                  )

    file_path = './src/data/carton.csv'
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = DictReader(file)
        data_list = [
            {
                'carton_type': row['CARTONTYPE'],
                'length': float(row['LENGTH']),
                'width': float(row['WIDTH']),
                'height': float(row['HEIGHT']),
                'barcode': row['BARCODE'],
                'count': int(row['DISPLAYRFPACK']),
                'id': uuid.uuid4() if 'id' not in row else uuid.UUID(
                    row['id'])
            }
            for row in reader
        ]
        op.bulk_insert(carton_ware, data_list)
    sku_ware = op.create_table('sku_ware',
                               sa.Column('sku', sa.Text(), unique=True),
                               sa.Column('length',
                                         sa.Numeric(precision=5, scale=1),
                                         nullable=True),
                               sa.Column('width',
                                         sa.Numeric(precision=5, scale=1),
                                         nullable=True),
                               sa.Column('height',
                                         sa.Numeric(precision=5, scale=1),
                                         nullable=True),
                               sa.Column('weight',
                                         sa.Numeric(precision=5, scale=1),
                                         nullable=True),
                               sa.Column('count', sa.Integer(),
                                         nullable=True),
                               sa.Column('barcode', sa.Text(), nullable=True),
                               sa.Column('img', sa.Text(), nullable=True),
                               sa.Column('id', sa.UUID(), primary_key=True),
                               sa.PrimaryKeyConstraint('id'),
                               sa.UniqueConstraint('sku')
                               )

    file_path = './src/data/sku.csv'
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = DictReader(file)
        data_list = [
            {
                'sku': row['sku'],
                'length': float(row['a']),
                'width': float(row['b']),
                'height': float(row['c']),
                'weight': float(row['weight']),
                'count': int(row['in_stock']),
                'barcode': row['barcode'],
                'img': row['img'],
                'id': uuid.uuid4() if 'id' not in row else uuid.UUID(
                    row['id'])
            }
            for row in reader
        ]
        op.bulk_insert(sku_ware, data_list)
    sku_cargotype = op.create_table('sku_cargotype',
    sa.Column('sku', sa.Text(), nullable=False),
    sa.Column('cargotype', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cargotype'], ['cargotype_ware.cargotype'], ),
    sa.ForeignKeyConstraint(['sku'], ['sku_ware.sku'], ),
    sa.PrimaryKeyConstraint('sku', 'cargotype')
    )

    file_path = './src/data/sku_cargotypes.csv'
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = DictReader(file)
        data_list = [
            {
                'sku': row['sku'],
                'cargotype': int(row['cargotype']),
                'id': uuid.uuid4() if 'id' not in row else uuid.UUID(
                    row['id'])
            }
            for row in reader
        ]
        op.bulk_insert(sku_cargotype, data_list)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sku_cargotype')
    op.drop_table('sku_ware')
    op.drop_table('carton_ware')
    op.drop_table('cargotype_ware')
    # ### end Alembic commands ###
