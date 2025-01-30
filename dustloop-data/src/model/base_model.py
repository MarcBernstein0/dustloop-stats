from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel

class Character(SQLModel, table=True):
    """Character metadata and identifiers."""
    __tablename__ = "characters" # type: ignore
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    slug: str = Field(index=True, description="URL-friendly name (e.g. 'Sol_Badguy')")
    display_name: str = Field(description="Display name (e.g. 'Sol Badguy')")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class BaseModel(SQLModel):
    """Base model for all sql tables"""
    id: Optional[int] = Field(default=None, primary_key=True)
    character: str = Field(index=True)
    table_name: str = Field(index=True)
    table_type: str = Field(index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class BaseMoveModel(BaseModel):
    """Base Move Model for common fields in a chara move data"""
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