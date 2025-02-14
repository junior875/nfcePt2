"""create produtos table

Revision ID: 001
Revises: 
Create Date: 2024-02-09 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('produtos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=True),
        sa.Column('codigo', sa.String(length=60), nullable=False),
        sa.Column('ean', sa.String(length=14), nullable=True),
        sa.Column('descricao', sa.String(length=120), nullable=False),
        sa.Column('ncm', sa.String(length=8), nullable=False),
        sa.Column('cfop', sa.String(length=4), nullable=False),
        sa.Column('unidade_comercial', sa.String(length=6), nullable=False),
        sa.Column('valor_unitario', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('ean_tributavel', sa.String(length=14), nullable=True),
        sa.Column('unidade_tributavel', sa.String(length=6), nullable=True),
        sa.Column('valor_unitario_tributavel', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('codigo')
    )
    
    # Índices para melhorar performance
    op.create_index(op.f('ix_produtos_ean'), 'produtos', ['ean'], unique=False)
    op.create_index(op.f('ix_produtos_ncm'), 'produtos', ['ncm'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_produtos_ncm'), table_name='produtos')
    op.drop_index(op.f('ix_produtos_ean'), table_name='produtos')
    op.drop_table('produtos')