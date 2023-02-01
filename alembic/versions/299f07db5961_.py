"""empty message

Revision ID: 299f07db5961
Revises: 9f239df49243
Create Date: 2023-01-31 15:30:53.048898

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '299f07db5961'
down_revision = '9f239df49243'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_ticket_bus_id', table_name='ticket')
    op.drop_index('ix_ticket_number_of_passenger', table_name='ticket')
    op.drop_index('ix_ticket_user_id', table_name='ticket')
    op.drop_table('ticket')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ticket',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('number_of_passenger', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('bus_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('is_done', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['bus_id'], ['busschedule.id'], name='ticket_bus_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='ticket_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='ticket_pkey')
    )
    op.create_index('ix_ticket_user_id', 'ticket', ['user_id'], unique=False)
    op.create_index('ix_ticket_number_of_passenger', 'ticket', ['number_of_passenger'], unique=False)
    op.create_index('ix_ticket_bus_id', 'ticket', ['bus_id'], unique=False)
    # ### end Alembic commands ###