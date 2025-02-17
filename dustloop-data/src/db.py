import os

from sqlalchemy import Engine
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
        self.engine = None
    
    def init_db(self):
        """Create the SQL Tables"""
        self.engine = create_engine(self.database_url)
        SQLModel.metadata.create_all(self.engine)

    def get_engine(self) -> Engine:
        if self.engine is None:
            self.engine = create_engine(self.database_url)
        return self.engine