"""Data migration

Revision ID: e6b0d51b901e
Revises: e90ced86cc0a
Create Date: 2023-06-15 14:33:20.573973

"""
import json
from pathlib import Path

from alembic import op

from src.core.settings import BASE_DIR
from src.db.models import Carton, Item, Prompt

# revision identifiers, used by Alembic.
revision = "e6b0d51b901e"
down_revision = "7b33ed336f6e"
branch_labels = None
depends_on = None

DATA_DIR = BASE_DIR / Path("data")
TABLES = [Item, Carton, Prompt]


def read_json(file_name):
    with open(file_name, "r") as fp:
        data = json.load(fp)
    return data


def upgrade() -> None:

    for table in TABLES:
        data_file = DATA_DIR / Path(table.__tablename__ + ".json")
        data = read_json(data_file)
        op.bulk_insert(table.__table__, data)


def downgrade() -> None:
    for table in TABLES:
        op.execute(f"DELETE FROM {table.__tablename__}")
