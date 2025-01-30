from typing import List, Optional
from sqlalchemy import JSON
from sqlmodel import Field
from ..base_model import BaseMoveModel

class BaseMoveData(BaseMoveModel):
    """Base class for all GGST move data tables"""
    pass
    # TODO: Implement table

class NormalMoves(BaseMoveData, table=True):
    """Normal move frame data."""
    __tablename__ = "normal_moves" # type: ignore
    # TODO: Implement table

class SpecialMoves(BaseMoveData, table=True):
    """Special move frame data."""
    __tablename__ = "special_moves" # type: ignore
    # TODO: Implement table

class OverdriveMoves(BaseMoveData, table=True):
    """Special move frame data."""
    __tablename__ = "overdrive_moves" # type: ignore
    # TODO: Implement table
    