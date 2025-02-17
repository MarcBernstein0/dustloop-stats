import os

from models import SystemCoreData
from sqlmodel import SQLModel, create_engine

from .model.ggst.moves import (
    NormalMoves,
    SpecialMoves,
    OverdriveMoves,
    SystemCoreData,
    SystemJumpData,
    GatlingModel,
    CharacterSpecificModel
)

class db:
    def __init__(self):
        """Initialize database connection"""
        self.database_url = os.getenv(
            "DATABASE_URL",
            "postgresql://postgres:postgres@localhost:5432/frame_data"
        )
        self.engine = create_engine(self.database_url)
    
    def init_db(self):
        """Create the SQL Tables"""
        SQLModel.metadata.create_all(self.engine)
