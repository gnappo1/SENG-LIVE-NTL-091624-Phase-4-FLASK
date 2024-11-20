"""create models

Revision ID: 447d8d27a851
Revises: 
Create Date: 2024-11-19 11:14:19.142038

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '447d8d27a851'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('productions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=80), nullable=False),
    sa.Column('genre', sa.String(length=20), nullable=False),
    sa.Column('director', sa.String(length=20), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('budget', sa.Float(), nullable=True),
    sa.Column('image', sa.String(), nullable=True),
    sa.Column('ongoing', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_productions')),
    sa.UniqueConstraint('title', 'director', name=op.f('uq_productions_title'))
    )
    op.create_table('crew_members',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('role', sa.String(length=40), nullable=False),
    sa.Column('production_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.ForeignKeyConstraint(['production_id'], ['productions.id'], name=op.f('fk_crew_members_production_id_productions')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_crew_members'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('crew_members')
    op.drop_table('productions')
    # ### end Alembic commands ###