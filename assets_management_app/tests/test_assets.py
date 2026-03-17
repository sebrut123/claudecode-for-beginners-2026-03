import pytest
from fastapi.testclient import TestClient

from app.main import app
import app.store as store_module


@pytest.fixture(autouse=True)
def clear_store():
    store_module.assets.clear()
    yield
    store_module.assets.clear()


client = TestClient(app)


def test_list_assets_empty():
    response = client.get("/assets")
    assert response.status_code == 200
    assert response.json() == []


def test_add_asset_returns_201():
    payload = {"name": "ThinkPad X1", "asset_type": "hardware", "description": "Laptop"}
    response = client.post("/assets", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "ThinkPad X1"
    assert data["asset_type"] == "hardware"
    assert data["description"] == "Laptop"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data
    assert data["os_info"] is None


def test_add_asset_with_os_info():
    payload = {
        "name": "ThinkPad X1",
        "asset_type": "hardware",
        "os_info": {"name": "Linux", "version": "Ubuntu 24.04"},
    }
    response = client.post("/assets", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["os_info"]["name"] == "Linux"
    assert data["os_info"]["version"] == "Ubuntu 24.04"


def test_list_assets_after_add():
    payload = {"name": "VS Code", "asset_type": "software"}
    client.post("/assets", json=payload)
    response = client.get("/assets")
    assert response.status_code == 200
    assets = response.json()
    assert len(assets) == 1
    assert assets[0]["name"] == "VS Code"


def test_add_asset_missing_required_field():
    response = client.post("/assets", json={"asset_type": "hardware"})
    assert response.status_code == 422


# --- helpers ---

def _create_asset(name="ThinkPad X1", asset_type="hardware"):
    resp = client.post("/assets", json={"name": name, "asset_type": asset_type})
    assert resp.status_code == 201
    return resp.json()


# --- get by ID ---

def test_get_asset_by_id():
    asset = _create_asset()
    response = client.get(f"/assets/{asset['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == asset["id"]


def test_get_asset_not_found():
    response = client.get("/assets/nonexistent-id")
    assert response.status_code == 404


# --- tags ---

def test_add_tags():
    asset = _create_asset()
    response = client.post(f"/assets/{asset['id']}/tags", json={"tags": ["critical", "finance"]})
    assert response.status_code == 200
    assert set(response.json()["tags"]) == {"critical", "finance"}


def test_add_tags_are_deduped():
    asset = _create_asset()
    client.post(f"/assets/{asset['id']}/tags", json={"tags": ["critical"]})
    response = client.post(f"/assets/{asset['id']}/tags", json={"tags": ["critical", "finance"]})
    assert response.json()["tags"].count("critical") == 1


def test_add_tags_to_missing_asset():
    response = client.post("/assets/nonexistent-id/tags", json={"tags": ["critical"]})
    assert response.status_code == 404


# --- activate / deactivate ---

def test_deactivate_asset_hidden_from_list():
    asset = _create_asset()
    client.patch(f"/assets/{asset['id']}/status", json={"active": False, "by": "admin"})
    assets = client.get("/assets").json()
    assert all(a["id"] != asset["id"] for a in assets)


def test_inactive_asset_visible_with_flag():
    asset = _create_asset()
    client.patch(f"/assets/{asset['id']}/status", json={"active": False, "by": "admin"})
    assets = client.get("/assets?include_inactive=true").json()
    assert any(a["id"] == asset["id"] for a in assets)


def test_deactivate_records_who_and_when():
    asset = _create_asset()
    response = client.patch(f"/assets/{asset['id']}/status", json={"active": False, "by": "admin"})
    data = response.json()
    assert data["is_active"] is False
    assert data["deactivated_by"] == "admin"
    assert data["deactivated_at"] is not None


def test_reactivate_asset_appears_in_list():
    asset = _create_asset()
    client.patch(f"/assets/{asset['id']}/status", json={"active": False, "by": "admin"})
    client.patch(f"/assets/{asset['id']}/status", json={"active": True, "by": "admin"})
    assets = client.get("/assets").json()
    assert any(a["id"] == asset["id"] for a in assets)


def test_deactivate_missing_asset():
    response = client.patch("/assets/nonexistent-id/status", json={"active": False, "by": "admin"})
    assert response.status_code == 404


# --- decommission ---

def test_decommission_asset():
    asset = _create_asset()
    response = client.post(f"/assets/{asset['id']}/decommission", json={"by": "admin"})
    assert response.status_code == 200
    data = response.json()
    assert data["decommissioned"] is True
    assert data["decommissioned_by"] == "admin"
    assert data["decommissioned_at"] is not None


def test_decommissioned_asset_hidden_from_list():
    asset = _create_asset()
    client.post(f"/assets/{asset['id']}/decommission", json={"by": "admin"})
    assets = client.get("/assets").json()
    assert all(a["id"] != asset["id"] for a in assets)


def test_decommissioned_asset_hidden_even_with_include_inactive():
    asset = _create_asset()
    client.post(f"/assets/{asset['id']}/decommission", json={"by": "admin"})
    assets = client.get("/assets?include_inactive=true").json()
    assert all(a["id"] != asset["id"] for a in assets)


def test_decommissioned_asset_retrievable_by_id():
    asset = _create_asset()
    client.post(f"/assets/{asset['id']}/decommission", json={"by": "admin"})
    response = client.get(f"/assets/{asset['id']}")
    assert response.status_code == 200
    assert response.json()["decommissioned"] is True


def test_decommission_twice_returns_409():
    asset = _create_asset()
    client.post(f"/assets/{asset['id']}/decommission", json={"by": "admin"})
    response = client.post(f"/assets/{asset['id']}/decommission", json={"by": "admin"})
    assert response.status_code == 409


def test_decommission_missing_asset():
    response = client.post("/assets/nonexistent-id/decommission", json={"by": "admin"})
    assert response.status_code == 404


def test_cannot_change_status_of_decommissioned_asset():
    asset = _create_asset()
    client.post(f"/assets/{asset['id']}/decommission", json={"by": "admin"})
    response = client.patch(f"/assets/{asset['id']}/status", json={"active": True, "by": "admin"})
    assert response.status_code == 409
