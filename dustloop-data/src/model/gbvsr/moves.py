from typing import List, Optional
from sqlalchemy import JSON
from sqlmodel import Field
from ..base_model import BaseMoveModel

class BaseMoveData(BaseMoveModel):
    """Base class for all GBVSR move data tables"""
    invuln: Optional[str] = Field(default=None, description="Invulnerability frames or properties")
    cooldown: Optional[str] = Field(default=None, description="Cooldown for the move")
    notes: Optional[str] = Field(default=None, description="Additional notes about the move")
    properties: Optional[List[str]] = Field(default=None, sa_type=JSON, description="Special properties of the move")


class NormalMoves(BaseMoveData, table=True):
    """Normal move frame data."""
    __tablename__ = "normal_moves" # type: ignore

class SpecialMoves(BaseMoveData, table=True):
    """Special move frame data."""
    __tablename__ = "special_moves" # type: ignore
    name: str = Field(description="Name of special move")
    meter_cost: Optional[str] = Field(default=None, description="Meter cost to perform the move")

class SuperMoves(BaseMoveData, table=True):
    """Special move frame data."""
    __tablename__ = "super_moves" # type: ignore
    name: str = Field(description="Name of the super move")
    meter_cost: Optional[str] = Field(default=None, description="Meter cost to perform the move")