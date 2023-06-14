"""Data migration

Revision ID: e6b0d51b901e
Revises: e90ced86cc0a
Create Date: 2023-06-13 12:03:20.573973

"""
import csv
from pathlib import Path

from alembic import op

from src.core.settings import BASE_DIR
from src.db.models import SKU, Carton, Prompt

# revision identifiers, used by Alembic.
revision = "e6b0d51b901e"
down_revision = "e90ced86cc0a"
branch_labels = None
depends_on = None

DATA_DIR = BASE_DIR / Path("data")
TABLES = [SKU, Carton, Prompt]


def read_csv(file_name):
    with open(file_name, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        rows = [r for r in reader]
    return rows


def upgrade() -> None:

    for table in TABLES:
        data_file = DATA_DIR / Path(table.__tablename__ + ".csv")
        rows = read_csv(data_file)
        op.bulk_insert(table.__table__, rows)


def downgrade() -> None:
    for table in TABLES:
        op.execute(f"DELETE FROM {table.__tablename__}")
