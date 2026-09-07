"""Saved import parameter presets (format_interchange_plan.md Sec 1.3, replacing `IGES.INI`) --
`GET/POST /import-profiles`, `PUT /import-profiles/{id}`. A caller passes `import_profile_id` on
`POST /import/iges` (see app/api/import_.py) instead of repeating every option field."""

import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.audit import record_audit
from app.deps import get_db
from app.errors import not_found
from app.models import ImportProfile
from app.permissions import require_import
from app.schemas import ImportProfileIn, ImportProfileOut

router = APIRouter(tags=["import-profiles"])


def _out(profile: ImportProfile) -> ImportProfileOut:
    return ImportProfileOut(
        id=str(profile.id), name=profile.name, trading_partner=profile.trading_partner, params=profile.params
    )


@router.get("/import-profiles", response_model=list[ImportProfileOut])
def list_import_profiles(actor: dict = Depends(require_import), db: Session = Depends(get_db)):
    rows = (
        db.query(ImportProfile)
        .filter(ImportProfile.organization_id == uuid.UUID(actor["organization_id"]))
        .order_by(ImportProfile.created_at.desc())
        .all()
    )
    return [_out(r) for r in rows]


@router.post("/import-profiles", response_model=ImportProfileOut)
def create_import_profile(body: ImportProfileIn, actor: dict = Depends(require_import), db: Session = Depends(get_db)):
    profile = ImportProfile(
        id=uuid.uuid4(),
        organization_id=uuid.UUID(actor["organization_id"]),
        name=body.name,
        trading_partner=body.trading_partner,
        params=body.params,
        created_by=uuid.UUID(actor["id"]),
    )
    db.add(profile)
    db.flush()
    record_audit(db, actor, "import_profile.create", "import_profile", profile.id, {"name": profile.name})
    return _out(profile)


@router.put("/import-profiles/{profile_id}", response_model=ImportProfileOut)
def update_import_profile(
    profile_id: str, body: ImportProfileIn, actor: dict = Depends(require_import), db: Session = Depends(get_db)
):
    profile = db.get(ImportProfile, uuid.UUID(profile_id))
    if profile is None or str(profile.organization_id) != actor["organization_id"]:
        raise not_found("Import profile")
    profile.name = body.name
    profile.trading_partner = body.trading_partner
    profile.params = body.params
    db.flush()
    record_audit(db, actor, "import_profile.update", "import_profile", profile.id, {"name": profile.name})
    return _out(profile)
