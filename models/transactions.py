import sqlalchemy as sa
from database import metadata

transactions = sa.Table('transactions',
                  metadata,
                  sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
                  sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id') ,nullable=False),
                  sa.Column('type', sa.String, nullable=False),
                  sa.Column('value', sa.Float, nullable=False),
                  sa.Column('receiver_id', sa.Integer, nullable=True),
                  sa.Column('created_at', sa.DateTime, server_default=sa.func.now())
                  )