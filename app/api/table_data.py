from flask import Blueprint, jsonify, request
from flask_login import login_required

from app.models import AnnotationTracking

api_bp = Blueprint("api", __name__, static_url_path="api")


@api_bp.route("/")
def api():
    return jsonify({"message": "Hello, World!"})


@api_bp.route("/table-data")
@login_required
def table_data():
    query = AnnotationTracking.query

    search = request.args.get('search')
    if search:
        query = query.filter(AnnotationTracking.name.contains(search))
    total = query.count()

    sort = request.args.get('sort')
    if sort:
        order = []
        for s in sort.split(','):
            if s.startswith('-'):
                order.append(getattr(getattr(AnnotationTracking, s[1:]), 'desc')())
            else:
                order.append(getattr(AnnotationTracking, s))
        query = query.order_by(*order)

    start = request.args.get('start', type=int, default=-1)
    length = request.args.get('length', type=int, default=-1)
    if start >= 0 and length >= 0:
        query = query.offset(start).limit(length)

    return jsonify({
        'data': [row.to_dict() for row in query.all()],
        'total': total,
    })
