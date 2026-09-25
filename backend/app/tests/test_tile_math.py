from app.engines.tile_math import layout_preview, tile_count


def test_guest_room_600_waste8():
    r = tile_count(6.0, 4.5, 0.6, 0.6, 8.0)
    assert r["area_m2"] == 27.0
    assert r["raw_count"] == 75
    assert r["order_count"] == 81
    assert r["layout"]["cols"] == 10
    assert r["layout"]["rows"] == 8
    assert r["layout"]["grid_count"] == 80


def test_layout_preview_small_room():
    lp = layout_preview(2.5, 2.0, 0.6, 0.6)
    assert lp["cols"] == 5
    assert lp["rows"] == 4
    assert lp["grid_count"] == 20


def test_zero_waste():
    r = tile_count(3.0, 3.0, 1.0, 1.0, 0.0)
    assert r["raw_count"] == 9
    assert r["order_count"] == 9


def test_non_rotated_matches_legacy():
    r = tile_count(2.5, 2.0, 0.6, 0.4, 8.0, rotated=False)
    assert r["rotated"] is False
    assert r["layout"] == {"cols": 5, "rows": 5, "grid_count": 25}
    legacy = tile_count(2.5, 2.0, 0.6, 0.4, 8.0)
    for k in ("area_m2", "piece_m2", "raw_count", "order_count", "layout"):
        assert r[k] == legacy[k]


def test_rotated_swaps_grid_axes_with_ceil():
    straight = tile_count(2.5, 2.0, 0.6, 0.4, 0.0, rotated=False)
    rotated = tile_count(2.5, 2.0, 0.6, 0.4, 0.0, rotated=True)
    # area-method counts are rotation invariant
    assert rotated["rotated"] is True
    assert rotated["raw_count"] == straight["raw_count"] == 21
    assert rotated["order_count"] == straight["order_count"] == 21
    # 2.5/0.4 -> 7 cols (ceil 6.25), 2.0/0.6 -> 4 rows (ceil 3.33)
    assert rotated["layout"] == {"cols": 7, "rows": 4, "grid_count": 28}
    assert straight["layout"] == {"cols": 5, "rows": 5, "grid_count": 25}


def test_rotated_square_tile_keeps_grid_but_marks_orientation():
    r = tile_count(6.0, 4.5, 0.6, 0.6, 8.0, rotated=True)
    assert r["rotated"] is True
    assert r["layout"] == {"cols": 10, "rows": 8, "grid_count": 80}
