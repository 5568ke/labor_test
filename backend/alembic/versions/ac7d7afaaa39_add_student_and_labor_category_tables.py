"""Add student and labor category tables

Revision ID: ac7d7afaaa39
Revises: 
Create Date: 2024-03-04 08:41:50.145427

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ac7d7afaaa39'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('labor_categories',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_labor_categories_id'), 'labor_categories', ['id'], unique=False)
    op.create_index(op.f('ix_labor_categories_name'), 'labor_categories', ['name'], unique=False)
    op.create_table('students',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_students_id'), 'students', ['id'], unique=False)
    op.create_index(op.f('ix_students_name'), 'students', ['name'], unique=False)
    op.create_table('labor_records',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.Column('labor_category_id', sa.Integer(), nullable=True),
    sa.Column('date', sa.String(), nullable=True),
    sa.Column('time', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['labor_category_id'], ['labor_categories.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_labor_records_date'), 'labor_records', ['date'], unique=False)
    op.create_index(op.f('ix_labor_records_id'), 'labor_records', ['id'], unique=False)
    op.create_index(op.f('ix_labor_records_time'), 'labor_records', ['time'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_labor_records_time'), table_name='labor_records')
    op.drop_index(op.f('ix_labor_records_id'), table_name='labor_records')
    op.drop_index(op.f('ix_labor_records_date'), table_name='labor_records')
    op.drop_table('labor_records')
    op.drop_index(op.f('ix_students_name'), table_name='students')
    op.drop_index(op.f('ix_students_id'), table_name='students')
    op.drop_table('students')
    op.drop_index(op.f('ix_labor_categories_name'), table_name='labor_categories')
    op.drop_index(op.f('ix_labor_categories_id'), table_name='labor_categories')
    op.drop_table('labor_categories')
    # ### end Alembic commands ###
