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
    id: Optional[int] = Field(default=None, primary_key=True)
    character: str = Field(index=True)
    table_name: str = Field(index=True)
    table_type: str = Field(index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
