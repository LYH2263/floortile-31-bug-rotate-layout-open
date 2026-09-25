from app.config import DEFAULT_ROTATED, DEFAULT_WASTE_PCT
from app.db import connect


def get_all() -> dict:
    conn = connect()
    try:
        rows = conn.execute("SELECT key, value FROM settings").fetchall()
        out = {r["key"]: r["value"] for r in rows}
        if "waste_pct" not in out:
            out["waste_pct"] = str(DEFAULT_WASTE_PCT)
        if "default_rotated" not in out:
            out["default_rotated"] = "1" if DEFAULT_ROTATED else "0"
        return out
    finally:
        conn.close()


def get_waste_pct() -> float:
    raw = get_all().get("waste_pct", str(DEFAULT_WASTE_PCT))
    return float(raw)


def get_default_rotated() -> bool:
    """System-wide default orientation; used when a tile has no own preference."""
    return get_all().get("default_rotated", "1" if DEFAULT_ROTATED else "0") == "1"


def set_value(key: str, value: str) -> None:
    conn = connect()
    try:
        conn.execute(
            "INSERT INTO settings(key,value) VALUES(?,?) "
            "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (key, value),
        )
        conn.commit()
    finally:
        conn.close()
