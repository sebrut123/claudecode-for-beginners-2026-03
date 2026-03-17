import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.models import Asset, AssetCreate
from app.store import get_store

router = APIRouter(prefix="/assets", tags=["assets"])


def _get_or_404(asset_id: str) -> Asset:
    asset = get_store().get(asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


@router.get("", response_model=list[Asset])
def list_assets(include_inactive: bool = False):
    assets = get_store().values()
    return [a for a in assets if not a.decommissioned and (include_inactive or a.is_active)]


@router.post("", response_model=Asset, status_code=201)
def add_asset(payload: AssetCreate):
    now = datetime.now(timezone.utc)
    asset = Asset(
        id=str(uuid.uuid4()),
        created_at=now,
        updated_at=now,
        **payload.model_dump(),
    )
    get_store()[asset.id] = asset
    return asset


@router.get("/{asset_id}", response_model=Asset)
def get_asset(asset_id: str):
    return _get_or_404(asset_id)


class TagsPayload(BaseModel):
    tags: list[str]


@router.post("/{asset_id}/tags", response_model=Asset)
def add_tags(asset_id: str, payload: TagsPayload):
    asset = _get_or_404(asset_id)
    updated = asset.model_copy(update={
        "tags": list(set(asset.tags) | set(payload.tags)),
        "updated_at": datetime.now(timezone.utc),
    })
    get_store()[asset_id] = updated
    return updated


class StatusPayload(BaseModel):
    active: bool
    by: str


@router.patch("/{asset_id}/status", response_model=Asset)
def set_status(asset_id: str, payload: StatusPayload):
    asset = _get_or_404(asset_id)
    if asset.decommissioned:
        raise HTTPException(status_code=409, detail="Cannot change status of a decommissioned asset")
    now = datetime.now(timezone.utc)
    updates: dict = {"is_active": payload.active, "updated_at": now}
    if not payload.active:
        updates["deactivated_at"] = now
        updates["deactivated_by"] = payload.by
    updated = asset.model_copy(update=updates)
    get_store()[asset_id] = updated
    return updated


class DecommissionPayload(BaseModel):
    by: str


@router.post("/{asset_id}/decommission", response_model=Asset)
def decommission_asset(asset_id: str, payload: DecommissionPayload):
    asset = _get_or_404(asset_id)
    if asset.decommissioned:
        raise HTTPException(status_code=409, detail="Asset is already decommissioned")
    now = datetime.now(timezone.utc)
    updated = asset.model_copy(update={
        "decommissioned": True,
        "decommissioned_at": now,
        "decommissioned_by": payload.by,
        "updated_at": now,
    })
    get_store()[asset_id] = updated
    return updated
