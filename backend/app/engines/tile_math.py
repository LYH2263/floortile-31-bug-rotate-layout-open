"""Floor tile order count: area method + optional grid layout preview."""

from app.engines.helpers import ceil_units


def oriented_tile(tile_l: float, tile_w: float, rotated: bool) -> tuple[float, float]:
    """Effective (along-room-length, along-room-width) edge lengths.

    Rotating a tile 90° swaps its two edges. For square tiles the swap is a
    no-op but the orientation marker is still recorded.
    """
    if rotated:
        return float(tile_w), float(tile_l)
    return float(tile_l), float(tile_w)


def tile_count(
    room_l: float,
    room_w: float,
    tile_l: float,
    tile_w: float,
    waste_pct: float,
    rotated: bool = False,
) -> dict:
    """
    raw_count: ceil(room_area / tile_piece_area)
    order_count: ceil(raw * (1 + waste_pct/100))

    Rotation swaps the tile edges used by the grid layout; piece area and
    therefore the area-method counts are invariant under 90° rotation.
    """
    rotated = bool(rotated)
    area = float(room_l) * float(room_w)
    piece = float(tile_l) * float(tile_w)
    if piece <= 0 or area < 0:
        raise ValueError("invalid dimensions")
    eff_l, eff_w = oriented_tile(tile_l, tile_w, rotated)
    raw = ceil_units(area / piece)
    with_waste = ceil_units(raw * (1 + float(waste_pct) / 100.0))
    layout = layout_preview(room_l, room_w, eff_l, eff_w)
    return {
        "area_m2": round(area, 3),
        "piece_m2": round(piece, 4),
        "raw_count": raw,
        "waste_pct": float(waste_pct),
        "order_count": with_waste,
        "rotated": rotated,
        "layout": layout,
    }


def layout_preview(room_l: float, room_w: float, tile_l: float, tile_w: float) -> dict:
    """Grid count if tiles are laid on a full rectangular lattice (may exceed area method).

    ``tile_l`` runs along the room length (columns), ``tile_w`` along the
    room width (rows). Pass swapped edges to render a 90°-rotated layout.
    """
    cols = ceil_units(float(room_l) / float(tile_l))
    rows = ceil_units(float(room_w) / float(tile_w))
    grid_count = cols * rows
    return {
        "cols": cols,
        "rows": rows,
        "grid_count": grid_count,
    }
