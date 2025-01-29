from typing import Optional
from models import BaseTable
from sqlmodel import Field


class NormalsMoves(BaseTable, table=True):
    """Normal move table"""
    l_moves: Optional[str] = Field(default=None, description="Light button moves")
    m_moves: Optional[str] = Field(default=None, description="Medium button moves")
    h_moves: Optional[str] = Field(default=None, description="Heavy button moves")
    u_moves: Optional[str] = Field(default=None, description="Unique button moves")
    cancel_options: Optional[str] = Field(default=None, description="Available cancel options")