import sqlalchemy as sa
from database import metadata

users = sa.Table('users',
                  metadata,
                  sa.Column('id', sa.Integer, primary_key=True),
                  sa.Column('name', sa.String(50), nullable=False, unique=True),
                  sa.Column('balance', sa.Integer, nullable=False)
                  )