"""Init

Revision ID: cac572444359
Revises: 
Create Date: 2023-11-10 21:11:12.357677

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'cac572444359'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass