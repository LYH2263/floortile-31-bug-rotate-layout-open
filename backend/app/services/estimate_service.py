from fastapi import HTTPException

from app.engines.tile_math import tile_count
from app.repositories import history, rooms, settings_repo, tiles


def resolve_rotated(tile: dict, requested: bool | None) -> bool:
    """Orientation resolution: request override > tile preference > system default.

    A tile with NULL ``default_rotated`` defers to the system-wide setting.
    """
    if requested is not None:
        return bool(requested)
    pref = tile.get("default_rotated")
    if pref is not None:
        return bool(pref)
    return settings_repo.get_default_rotated()


def run_estimate(
    room_id: int,
    tile_id: int,
    waste_pct: float | None,
    save: bool,
    note: str,
    rotated: bool | None = None,
):
    room = rooms.get_room(room_id)
    if not room:
        raise HTTPException(404, "room not found")
    tile = tiles.get_tile(tile_id)
    if not tile:
        raise HTTPException(404, "tile not found")
    if room.get("data_quality") == "dirty":
        raise HTTPException(422, "room marked dirty; fix dimensions before estimate")

    waste = float(waste_pct) if waste_pct is not None else settings_repo.get_waste_pct()
    oriented = resolve_rotated(tile, rotated)
    calc = tile_count(
        room["length"], room["width"], tile["tile_l"], tile["tile_w"], waste, oriented
    )

    run_id = None
    if save:
        # calc already carries rotated/layout/order_count; the snapshot is
        # immutable and is never recomputed when defaults change later.
        payload = {**calc, "room_id": room_id, "tile_id": tile_id}
        run_id = history.insert_run(room_id, tile_id, waste, payload, note)

    return {
        "room_id": room_id,
        "tile_id": tile_id,
        "room": room,
        "tile": tile,
        "run_id": run_id,
        **calc,
    }
