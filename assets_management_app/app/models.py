from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class OsInfo(BaseModel):
    name: str
    version: str


class AssetCreate(BaseModel):
    name: str
    asset_type: str
    description: str = ""
    os_info: Optional[OsInfo] = None


class Asset(AssetCreate):
    id: str
    created_at: datetime
    updated_at: datetime
    tags: list[str] = []
    is_active: bool = True
    deactivated_at: Optional[datetime] = None
    deactivated_by: Optional[str] = None
    decommissioned: bool = False
    decommissioned_at: Optional[datetime] = None
    decommissioned_by: Optional[str] = None
