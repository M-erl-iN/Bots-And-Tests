from flask import Blueprint, jsonify, request

from . import db_session
from .jobs import Jobs

blueprint = Blueprint("jobs_api", __name__, template_folder="templates")
job_parameters = [
    "id",
    "team_leader",
    "job",
    "work_size",
    "collaborators",
    "start_date",
    "end_date",
    "is_finished",
    "creator",
]


@blueprint.route("/api/jobs")
def get_jobs():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return jsonify(
        {
            "jobs": [
                item.to_dict(
                    only=(
                        "id",
                        "team_leader",
                        "job",
                        "work_size",
                        "collaborators",
                        "start_date",
                        "end_date",
                        "is_finished",
                    )
                )
                for item in jobs
            ]
        }
    )


@blueprint.route("/api/jobs/<jobs_id>", methods=["GET"])
def get_one_jobs(jobs_id):
    session = db_session.create_session()
    try:
        jobs = session.query(Jobs).get(int(jobs_id))
    except ValueError:
        return jsonify({"error": "Not found"})
    if not jobs:
        return jsonify({"error": "Not found"})
    return jsonify(
        {
            "jobs": jobs.to_dict(
                only=(
                    "id",
                    "team_leader",
                    "job",
                    "work_size",
                    "collaborators",
                    "start_date",
                    "end_date",
                    "is_finished",
                )
            )
        }
    )


@blueprint.route("/api/jobs", methods=["POST"])
def create_jobs():
    if not request.json:
        return jsonify({"error": "Empty request"})
    elif not all(key in request.json for key in job_parameters):
        return jsonify({"error": "Bad request"})
    session = db_session.create_session()
    if session.query(Jobs).get(request.json["id"]):
        return jsonify({"error": "Id already exists"})
    jobs = Jobs(
        id=request.json["id"],
        team_leader=request.json["team_leader"],
        job=request.json["job"],
        work_size=request.json["work_size"],
        collaborators=request.json["collaborators"],
        start_date=request.json["start_date"],
        end_date=request.json["end_date"],
        is_finished=request.json["is_finished"],
        creator=request.json["creator"],
    )
    session.add(jobs)
    session.commit()
    return jsonify({"success": "OK"})
