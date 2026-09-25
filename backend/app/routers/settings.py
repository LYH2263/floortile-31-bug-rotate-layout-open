from fastapi import APIRouter

from app.repositories import settings_repo
from app.schemas.estimate import SettingsUpdate

router = APIRouter(tags=["settings"])


@router.get("/settings")
def get_settings():
    return settings_repo.get_all()


@router.patch("/settings")
def update_settings(body: SettingsUpdate):
    """Update system-wide defaults.

    Only affects new estimates; saved calc runs keep their own snapshots.
    """
    if body.waste_pct is not None:
        settings_repo.set_value("waste_pct", str(float(body.waste_pct)))
    if body.default_rotated is not None:
        settings_repo.set_value(
            "default_rotated", "1" if body.default_rotated else "0"
        )
    return settings_repo.get_all()
