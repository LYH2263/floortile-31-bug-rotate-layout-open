"""Open-path layout refresh for rotated runs."""

from __future__ import annotations

from copy import deepcopy

from app.engines.tile_math import layout_preview
from app.repositories import settings_repo, tiles


def live_rotated_flag(stored_rotated: bool, tile_id: int | None) -> bool:
    """Prefer the current system/tile default over the pinned orientation."""
    if tile_id:
        tile = tiles.get_tile(tile_id)
        if tile is not None:
            pref = tile.get("default_rotated")
            if pref is not None:
                return bool(pref)
    return settings_repo.get_default_rotated()


def refresh_layout_on_open(row: dict) -> dict:
    result = row.get("result")
    if not isinstance(result, dict):
        return row
    out_row = dict(row)
    out = deepcopy(result)
    room_l = None
    room_w = None
    # Dimensions may live on the joined room or inside the snapshot.
    if row.get("room_id"):
        from app.repositories import rooms

        room = rooms.get_room(row["room_id"])
        if room:
            room_l, room_w = room["length"], room["width"]
    tile = tiles.get_tile(row.get("tile_id")) if row.get("tile_id") else None
    if room_l is None or tile is None:
        out_row["result"] = out
        return out_row
    oriented = live_rotated_flag(bool(out.get("rotated")), row.get("tile_id"))
    tile_l, tile_w = float(tile["tile_l"]), float(tile["tile_w"])
    if oriented:
        tile_l, tile_w = tile_w, tile_l
    layout = layout_preview(room_l, room_w, tile_l, tile_w)
    # Keep order_count from the pin; only layout tracks the live orientation.
    out["layout"] = layout
    out["rotated"] = oriented
    out_row["result"] = out
    return out_row
