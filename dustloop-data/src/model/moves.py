from typing import List, Optional
from models import BaseTable
from sqlmodel import Field, SQLModel

class BaseMoveData(BaseTable):
    """Base class for all move data tables"""
    input: str = Field(description="Input command for the move")
    damage: Optional[str] =  Field(default=None, description="Base damage of the move (can be a range or formula)")
    guard: Optional[str] = Field(default=None, description="Guard type (All, High, Low, etc)")
    startup: Optional[str] = Field(default=None, description="Startup frames (can be a range)")
    active: Optional[str] = Field(default=None, description="Active frames (can be a range or list)")
    recovery: Optional[str] = Field(default=None, description="Recovery frames (can be a range)")
    on_block: Optional[str] = Field(default=None, description="Frame advantage on block (can be +/- or special values)")
    on_hit: Optional[str] = Field(default=None, description="Frame advantage on hit (can be +/- or special values)")
    level: Optional[str] = Field(default=None, description="Attack level (can include special properties)")
    counter_type: Optional[str] = Field(default=None, description="Counter hit type")
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