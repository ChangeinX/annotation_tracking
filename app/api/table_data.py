import datetime

from flask import Blueprint, jsonify, request, abort
from flask_login import login_required, current_user

from app import db
from app.models import AnnotationTracking

api_bp = Blueprint("api", __name__, static_url_path="api")


@api_bp.route("/")
@login_required
def api():
    return jsonify({"message": "Hello, World!"})


@api_bp.route("/table-data")
@login_required
def table_data():
    query = AnnotationTracking.query

    search = request.args.get("search")
    if search:
        query = query.filter(
            AnnotationTracking.site_id.ilike(f"%{search}%")
            | AnnotationTracking.donation_id.ilike(f"%{search}%")
            | AnnotationTracking.video_id.ilike(f"%{search}%")
            | AnnotationTracking.segment_id.ilike(f"%{search}%")
            | AnnotationTracking.stage.ilike(f"%{search}%")
            | AnnotationTracking.video_length.ilike(f"%{search}%")
            | AnnotationTracking.assigned_on.ilike(f"%{search}%")
            | AnnotationTracking.assigned_to.ilike(f"%{search}%")
        )
    total = query.count()

    sort = request.args.get("sort")
    if sort:
        order = []
        for s in sort.split(","):
            direction = s[0]
            identifier = s[1:]
            if identifier not in ["site_id", "segment_id" "donation_id", "video_id"]:
                identifier = "id"
            col = getattr(AnnotationTracking, identifier)
            if direction == "-":
                col = col.desc()
            order.append(col)
        if order:
            query = query.order_by(*order)

    start = request.args.get("start", type=int, default=-1)
    length = request.args.get("length", type=int, default=-1)
    if start >= 0 and length >= 0:
        query = query.offset(start).limit(length)

    return jsonify(
        {
            "data": [row.to_dict() for row in query.all()],
            "total": total,
        }
    )


@api_bp.route("/table-data", methods=["POST"])
@login_required
def update_table_data():
    data = request.get_json()
    print(f'update_table_data: {data}')
    if "id" not in data:
        print("No id provided")
        abort(401, "No id provided")
    else:
        print(f'update_table_data: {data["id"]}')
        annotation_record = AnnotationTracking.query.filter_by(id=data["id"])
        if not annotation_record:
            return jsonify({"message": "Record not found"}), 404

        fields = [
            'site_id',
            'donation_id',
            'video_id',
            'segment_id',
            'stage',
            'video_length',
            'assigned_on',
            'assigned_to',
        ]

        for field in fields:
            if field == data['column']:
                annotation_record.update({field: data["value"]})

        db.session.commit()
    return jsonify({"message": "Record updated"}), 200


@api_bp.route("/add-record", methods=["POST"])
@login_required
def add_record():
    data = request.get_json()
    print(f'add_record: {data}')
    if "site_id" not in data:
        print("No site_id provided")
        abort(401, "No site_id provided")
    else:
        # SQLite DateTime type only accepts Python datetime and date objects as input.
        # create timestamp
        assigned_on = datetime.datetime.now()
        annotation_record = AnnotationTracking(
            user_id=current_user.id,
            site_id=data["site_id"],
            donation_id=data["donation_id"],
            video_id=data["video_id"],
            segment_id=data["segment_id"],
            stage=data["stage"],
            video_length=data["video_length"],
            assigned_on=assigned_on,
            assigned_to=data["assigned_to"],
        )
        db.session.add(annotation_record)
        db.session.commit()
    return jsonify({"message": "Record added"}), 200
