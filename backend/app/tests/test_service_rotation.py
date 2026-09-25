import pytest

from app import seed
from app.db import connect
from app.repositories import history, settings_repo
from app.services import estimate_service


@pytest.fixture()
def db(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setattr("app.db.DB_PATH", db_path)
    seed.init_db()
    return db_path


def test_tile_preference_overrides_system_default(db):
    # tile 3 (300x600木纹) has default_rotated=0 even if system default flips
    settings_repo.set_value("default_rotated", "1")
    r = estimate_service.run_estimate(1, 3, None, False, "")
    assert r["rotated"] is False


def test_system_default_used_when_tile_pref_null(db):
    settings_repo.set_value("default_rotated", "0")
    r0 = estimate_service.run_estimate(1, 1, None, False, "")
    assert r0["rotated"] is False
    settings_repo.set_value("default_rotated", "1")
    r1 = estimate_service.run_estimate(1, 1, None, False, "")
    assert r1["rotated"] is True


def test_request_orientation_wins_and_swaps_grid(db):
    # room 6.0x4.5, tile 3 = 0.6x0.3
    straight = estimate_service.run_estimate(1, 3, None, False, "", rotated=False)
    assert straight["layout"] == {"cols": 10, "rows": 15, "grid_count": 150}
    turned = estimate_service.run_estimate(1, 3, None, False, "", rotated=True)
    assert turned["rotated"] is True
    # 6/0.3 -> 20 cols, 4.5/0.6 -> 8 rows (both ceil)
    assert turned["layout"] == {"cols": 20, "rows": 8, "grid_count": 160}


def test_saved_run_keeps_orientation_after_default_change(db):
    settings_repo.set_value("default_rotated", "0")
    saved = estimate_service.run_estimate(1, 1, None, True, "旧记录")
    run_id = saved["run_id"]
    assert saved["rotated"] is False

    # changing the system default must not recompute or alter the old run
    settings_repo.set_value("default_rotated", "1")
    old = history.get_run(run_id)
    assert old["result"]["rotated"] is False
    assert old["result"]["layout"] == saved["layout"]
    assert old["result"]["order_count"] == saved["order_count"]

    # new estimates use the new default
    fresh = estimate_service.run_estimate(1, 1, None, False, "")
    assert fresh["rotated"] is True
