"""Marker Making Sec 1.4/2 (new): matching rule tables. The platform stores and returns
offsets_json / stripe_definitions_json / stripe_marks_json / weave_line_json /
material_pattern_json faithfully -- it does not validate their internal shape (element ids,
offset-count caps, etc.); that interpretation lives in marker-making-service, per the same
opaque-payload philosophy as marker_pieces.placement_data.

Define Material / Material Pattern (Sec 1.4): a fabric reference image, uploaded the same way as
piece/marker versions (Section 3.3's SAS-URL flow -- the API never sees the image bytes). Unlike
piece/marker versions, a matching rule table has no version history for its material pattern, so
there's no intermediate DB row between begin-upload and complete -- the client carries
storage_container/storage_key forward from the begin-upload response and hands them back on
complete, and a re-upload just overwrites the same deterministic blob key."""

import uuid
from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends, Header, Query
from sqlalchemy.orm import Session

from app.auditing import record_audit
from app.deps import (
    Actor,
    check_if_match_version,
    get_current_actor,
    get_db,
    get_request_id,
    require_permission,
)
from app.errors import bad_request, conflict, not_found
from app.models import Marker, MatchingRuleTable
from app.schemas import (
    DownloadUrlResponse,
    JsonArrayReplace,
    MatchingRuleTableCreate,
    MatchingRuleTablePatch,
    MaterialPatternBeginRequest,
    MaterialPatternBeginResponse,
    MaterialPatternCompleteRequest,
    MaterialPatternVisibility,
    OffsetsReplace,
    Page,
    WeaveLineReplace,
)
from app.serializers import matching_rule_table_out
from app.storage import generate_download_sas_url, generate_upload_sas_url

router = APIRouter(prefix="/matching-rule-tables", tags=["matching-rule-tables"])

MATERIAL_PATTERN_STORAGE_CONTAINER = "dmp-matching"
_MATERIAL_PATTERN_EXTENSIONS = {"png": "png", "jpg": "jpg", "jpeg": "jpg", "webp": "webp"}


def _get_table_or_404(db: Session, table_id: uuid.UUID, org_id: uuid.UUID) -> MatchingRuleTable:
    row = db.get(MatchingRuleTable, table_id)
    if row is None or row.deleted_at is not None or row.organization_id != org_id:
        raise not_found("Matching rule table")
    return row


@router.get("", response_model=Page)
def list_matching_rule_tables(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    require_permission(
        db, actor, "matching_rule_table.read", request_id=request_id,
        entity_type="matching_rule_table", action="matching_rule_table.list",
    )
    query = db.query(MatchingRuleTable).filter(
        MatchingRuleTable.organization_id == actor.organization_id, MatchingRuleTable.deleted_at.is_(None)
    )
    total = query.count()
    rows = query.offset((page - 1) * page_size).limit(page_size).all()
    return Page(items=[matching_rule_table_out(db, r) for r in rows], page=page, page_size=page_size, total=total)


@router.post("", status_code=201)
def create_matching_rule_table(
    body: MatchingRuleTableCreate,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    require_permission(
        db, actor, "matching_rule_table.write", request_id=request_id,
        entity_type="matching_rule_table", action="matching_rule_table.create",
    )
    row = MatchingRuleTable(
        organization_id=actor.organization_id,
        name=body.name,
        method=body.method,
        plaid_repeat=body.plaid_repeat,
        stripe_repeat=body.stripe_repeat,
        created_by=actor.user_id,
        updated_by=actor.user_id,
    )
    db.add(row)
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="matching_rule_table.create",
        entity_type="matching_rule_table", entity_id=row.id, request_id=request_id,
        after_state={"name": row.name, "method": row.method}, result="success",
    )
    return matching_rule_table_out(db, row)


@router.get("/{table_id}")
def get_matching_rule_table(
    table_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    row = _get_table_or_404(db, table_id, actor.organization_id)
    require_permission(
        db, actor, "matching_rule_table.read", request_id=request_id,
        entity_type="matching_rule_table", action="matching_rule_table.read", entity_id=row.id,
    )
    return matching_rule_table_out(db, row)


@router.patch("/{table_id}")
def patch_matching_rule_table(
    table_id: uuid.UUID,
    body: MatchingRuleTablePatch,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
    if_match_version: int | None = Header(None, alias="If-Match-Version"),
):
    row = _get_table_or_404(db, table_id, actor.organization_id)
    require_permission(
        db, actor, "matching_rule_table.write", request_id=request_id,
        entity_type="matching_rule_table", action="matching_rule_table.update", entity_id=row.id,
    )
    check_if_match_version(if_match_version, row.version)

    before = {"name": row.name, "method": row.method}
    for field in ("name", "method", "plaid_repeat", "stripe_repeat"):
        value = getattr(body, field)
        if value is not None:
            setattr(row, field, value)
    row.updated_by = actor.user_id
    row.version += 1
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="matching_rule_table.update",
        entity_type="matching_rule_table", entity_id=row.id, request_id=request_id,
        before_state=before, after_state={"name": row.name, "method": row.method}, result="success",
    )
    return matching_rule_table_out(db, row)


@router.delete("/{table_id}", status_code=204)
def delete_matching_rule_table(
    table_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    row = _get_table_or_404(db, table_id, actor.organization_id)
    require_permission(
        db, actor, "matching_rule_table.delete", request_id=request_id,
        entity_type="matching_rule_table", action="matching_rule_table.delete", entity_id=row.id,
    )
    if db.query(Marker.id).filter_by(matching_rule_table_id=row.id).filter(Marker.deleted_at.is_(None)).first():
        raise conflict("Matching rule table is still referenced by a marker.")

    row.deleted_at = datetime.now(UTC)
    row.updated_by = actor.user_id
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="matching_rule_table.delete",
        entity_type="matching_rule_table", entity_id=row.id, request_id=request_id, result="success",
    )


@router.put("/{table_id}/offsets")
def replace_offsets(
    table_id: uuid.UUID,
    body: OffsetsReplace,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
    if_match_version: int | None = Header(None, alias="If-Match-Version"),
):
    row = _get_table_or_404(db, table_id, actor.organization_id)
    require_permission(
        db, actor, "matching_rule_table.write", request_id=request_id,
        entity_type="matching_rule_table", action="matching_rule_table.offsets.replace", entity_id=row.id,
    )
    check_if_match_version(if_match_version, row.version)
    row.offsets_json = {"horizontal": body.horizontal, "vertical": body.vertical}
    row.updated_by = actor.user_id
    row.version += 1
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id,
        action="matching_rule_table.offsets.replace", entity_type="matching_rule_table", entity_id=row.id,
        request_id=request_id, after_state=row.offsets_json, result="success",
    )
    return matching_rule_table_out(db, row)


@router.put("/{table_id}/stripe-definitions")
def replace_stripe_definitions(
    table_id: uuid.UUID,
    body: JsonArrayReplace,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
    if_match_version: int | None = Header(None, alias="If-Match-Version"),
):
    row = _get_table_or_404(db, table_id, actor.organization_id)
    require_permission(
        db, actor, "matching_rule_table.write", request_id=request_id,
        entity_type="matching_rule_table", action="matching_rule_table.stripe_definitions.replace",
        entity_id=row.id,
    )
    check_if_match_version(if_match_version, row.version)
    row.stripe_definitions_json = body.items
    row.updated_by = actor.user_id
    row.version += 1
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id,
        action="matching_rule_table.stripe_definitions.replace", entity_type="matching_rule_table",
        entity_id=row.id, request_id=request_id, after_state={"count": len(body.items)}, result="success",
    )
    return matching_rule_table_out(db, row)


@router.put("/{table_id}/stripe-marks")
def replace_stripe_marks(
    table_id: uuid.UUID,
    body: JsonArrayReplace,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
    if_match_version: int | None = Header(None, alias="If-Match-Version"),
):
    row = _get_table_or_404(db, table_id, actor.organization_id)
    require_permission(
        db, actor, "matching_rule_table.write", request_id=request_id,
        entity_type="matching_rule_table", action="matching_rule_table.stripe_marks.replace", entity_id=row.id,
    )
    check_if_match_version(if_match_version, row.version)
    row.stripe_marks_json = body.items
    row.updated_by = actor.user_id
    row.version += 1
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id,
        action="matching_rule_table.stripe_marks.replace", entity_type="matching_rule_table",
        entity_id=row.id, request_id=request_id, after_state={"count": len(body.items)}, result="success",
    )
    return matching_rule_table_out(db, row)


@router.put("/{table_id}/weave-line")
def replace_weave_line(
    table_id: uuid.UUID,
    body: WeaveLineReplace,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
    if_match_version: int | None = Header(None, alias="If-Match-Version"),
):
    row = _get_table_or_404(db, table_id, actor.organization_id)
    require_permission(
        db, actor, "matching_rule_table.write", request_id=request_id,
        entity_type="matching_rule_table", action="matching_rule_table.weave_line.replace", entity_id=row.id,
    )
    check_if_match_version(if_match_version, row.version)
    row.weave_line_json = {"angle_deg": body.angle_deg, "offset": body.offset, "visible": body.visible}
    row.updated_by = actor.user_id
    row.version += 1
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id,
        action="matching_rule_table.weave_line.replace", entity_type="matching_rule_table",
        entity_id=row.id, request_id=request_id, after_state=row.weave_line_json, result="success",
    )
    return matching_rule_table_out(db, row)


# -- Define Material / Material Pattern --------------------------------------------------------


@router.post("/{table_id}/material-pattern/begin-upload", response_model=MaterialPatternBeginResponse)
def begin_material_pattern_upload(
    table_id: uuid.UUID,
    body: MaterialPatternBeginRequest,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    row = _get_table_or_404(db, table_id, actor.organization_id)
    require_permission(
        db, actor, "matching_rule_table.write", request_id=request_id,
        entity_type="matching_rule_table", action="matching_rule_table.material_pattern.begin_upload",
        entity_id=row.id,
    )
    extension = _MATERIAL_PATTERN_EXTENSIONS.get(body.file_format.lower())
    if extension is None:
        raise bad_request(f"Unsupported file_format '{body.file_format}'; expected one of {sorted(_MATERIAL_PATTERN_EXTENSIONS)}.")
    blob_key = f"{actor.organization_id}/{row.id}/material-pattern.{extension}"
    expiry_minutes = 15
    upload_url = generate_upload_sas_url(MATERIAL_PATTERN_STORAGE_CONTAINER, blob_key, expiry_minutes=expiry_minutes)
    return MaterialPatternBeginResponse(
        upload_url=upload_url,
        storage_container=MATERIAL_PATTERN_STORAGE_CONTAINER,
        storage_key=blob_key,
        expires_at=datetime.now(UTC) + timedelta(minutes=expiry_minutes),
    )


@router.post("/{table_id}/material-pattern/complete")
def complete_material_pattern_upload(
    table_id: uuid.UUID,
    body: MaterialPatternCompleteRequest,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
    if_match_version: int | None = Header(None, alias="If-Match-Version"),
):
    row = _get_table_or_404(db, table_id, actor.organization_id)
    require_permission(
        db, actor, "matching_rule_table.write", request_id=request_id,
        entity_type="matching_rule_table", action="matching_rule_table.material_pattern.complete", entity_id=row.id,
    )
    check_if_match_version(if_match_version, row.version)
    row.material_pattern_json = {
        "name": body.material_name,
        "visible": True,
        "storage_container": body.storage_container,
        "storage_key": body.storage_key,
        "checksum_sha256": body.checksum_sha256,
    }
    row.updated_by = actor.user_id
    row.version += 1
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id,
        action="matching_rule_table.material_pattern.complete", entity_type="matching_rule_table",
        entity_id=row.id, request_id=request_id,
        after_state={"name": body.material_name, "storage_key": body.storage_key}, result="success",
    )
    return matching_rule_table_out(db, row)


@router.put("/{table_id}/material-pattern/visibility")
def set_material_pattern_visibility(
    table_id: uuid.UUID,
    body: MaterialPatternVisibility,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
    if_match_version: int | None = Header(None, alias="If-Match-Version"),
):
    row = _get_table_or_404(db, table_id, actor.organization_id)
    require_permission(
        db, actor, "matching_rule_table.write", request_id=request_id,
        entity_type="matching_rule_table", action="matching_rule_table.material_pattern.visibility",
        entity_id=row.id,
    )
    if row.material_pattern_json is None:
        raise conflict("No material pattern uploaded for this matching rule table yet.")
    check_if_match_version(if_match_version, row.version)
    row.material_pattern_json = {**row.material_pattern_json, "visible": body.visible}
    row.updated_by = actor.user_id
    row.version += 1
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id,
        action="matching_rule_table.material_pattern.visibility", entity_type="matching_rule_table",
        entity_id=row.id, request_id=request_id, after_state={"visible": body.visible}, result="success",
    )
    return matching_rule_table_out(db, row)


@router.get("/{table_id}/material-pattern/download-url", response_model=DownloadUrlResponse)
def get_material_pattern_download_url(
    table_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    row = _get_table_or_404(db, table_id, actor.organization_id)
    require_permission(
        db, actor, "matching_rule_table.read", request_id=request_id,
        entity_type="matching_rule_table", action="matching_rule_table.material_pattern.download_url",
        entity_id=row.id,
    )
    if row.material_pattern_json is None:
        raise not_found("Material pattern")
    expiry_minutes = 15
    url = generate_download_sas_url(
        row.material_pattern_json["storage_container"], row.material_pattern_json["storage_key"],
        expiry_minutes=expiry_minutes,
    )
    return DownloadUrlResponse(download_url=url, expires_at=datetime.now(UTC) + timedelta(minutes=expiry_minutes))


@router.delete("/{table_id}/material-pattern")
def delete_material_pattern(
    table_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
    if_match_version: int | None = Header(None, alias="If-Match-Version"),
):
    row = _get_table_or_404(db, table_id, actor.organization_id)
    require_permission(
        db, actor, "matching_rule_table.write", request_id=request_id,
        entity_type="matching_rule_table", action="matching_rule_table.material_pattern.delete", entity_id=row.id,
    )
    check_if_match_version(if_match_version, row.version)
    row.material_pattern_json = None
    row.updated_by = actor.user_id
    row.version += 1
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id,
        action="matching_rule_table.material_pattern.delete", entity_type="matching_rule_table",
        entity_id=row.id, request_id=request_id, result="success",
    )
    return matching_rule_table_out(db, row)
