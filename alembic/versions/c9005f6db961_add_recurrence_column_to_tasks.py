"""Add recurrence column to tasks

Revision ID: c9005f6db961
Revises: 
Create Date: 2024-03-07 11:31:53.645193

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c9005f6db961'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# def upgrade() -> None:
#     # ### commands auto generated by Alembic - please adjust! ###
#     op.create_table('tasks',
#     sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
#     sa.Column('name', sa.String(), nullable=False),
#     sa.Column('scheduled_time', sa.DateTime(), nullable=False),
#     sa.Column('recurrence', sa.Enum('ONCE', 'DAILY', 'WEEKLY', 'BIWEEKLY', 'MONTHLY', 'QUARTERLY', 'YEARLY', name='recurrencefrequency'), nullable=True),
#     sa.PrimaryKeyConstraint('id'),
#     sa.UniqueConstraint('name'),
#     schema='task_schema'
#     )
#     op.drop_table('tasks')
#     # ### end Alembic commands ###

def upgrade() -> None:
    # Execute a SQL statement to create the Enum type
    op.execute("CREATE TYPE recurrencefrequency AS ENUM ('ONCE', 'DAILY', 'WEEKLY', 'BIWEEKLY', 'MONTHLY', 'QUARTERLY', 'YEARLY')")
    
    # Now add the 'recurrence' column using the newly created Enum type
    op.add_column('tasks', sa.Column('recurrence', sa.Enum(name='recurrencefrequency'), nullable=True), schema='task_schema')


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tasks',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('scheduled_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='tasks_pkey'),
    sa.UniqueConstraint('name', name='tasks_name_key')
    )
    op.drop_table('tasks', schema='task_schema')
    # ### end Alembic commands ###
