"""add family trees and tree_id columns

Revision ID: c1a2b3d4e5f6
Revises: b5fc464cf5cb
Create Date: 2026-03-14 12:00:00.000000

This migration adds:
- family_trees table for multi-tenant tree isolation
- tree_id column to users, persons, and relationships tables
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c1a2b3d4e5f6'
down_revision: Union[str, Sequence[str], None] = 'b5fc464cf5cb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create family_trees table
    op.create_table('family_trees',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.String(length=500), nullable=True),
        sa.Column('owner_id', sa.UUID(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Add tree_id column to users table
    op.add_column('users', sa.Column('tree_id', sa.UUID(), nullable=True))
    op.create_foreign_key(
        'fk_users_tree_id',
        'users', 'family_trees',
        ['tree_id'], ['id']
    )
    
    # Add tree_id column to persons table
    op.add_column('persons', sa.Column('tree_id', sa.UUID(), nullable=True))
    op.create_foreign_key(
        'fk_persons_tree_id',
        'persons', 'family_trees',
        ['tree_id'], ['id']
    )
    
    # Add tree_id column to relationships table
    op.add_column('relationships', sa.Column('tree_id', sa.UUID(), nullable=True))
    op.create_foreign_key(
        'fk_relationships_tree_id',
        'relationships', 'family_trees',
        ['tree_id'], ['id']
    )
    
    # Add foreign key for owner_id in family_trees (after users table has tree_id)
    op.create_foreign_key(
        'fk_family_trees_owner_id',
        'family_trees', 'users',
        ['owner_id'], ['id']
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Remove foreign key constraints first
    op.drop_constraint('fk_family_trees_owner_id', 'family_trees', type_='foreignkey')
    op.drop_constraint('fk_relationships_tree_id', 'relationships', type_='foreignkey')
    op.drop_constraint('fk_persons_tree_id', 'persons', type_='foreignkey')
    op.drop_constraint('fk_users_tree_id', 'users', type_='foreignkey')
    
    # Remove tree_id columns
    op.drop_column('relationships', 'tree_id')
    op.drop_column('persons', 'tree_id')
    op.drop_column('users', 'tree_id')
    
    # Drop family_trees table
    op.drop_table('family_trees')
