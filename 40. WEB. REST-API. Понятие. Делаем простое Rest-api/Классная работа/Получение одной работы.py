from flask import Blueprint, Flask, jsonify, make_response

from . import db_session
from .jobs import Jobs

blueprint = Blueprint("jobs_api", __name__, template_folder="templates")


@blueprint.route("/api/jobs")
def get_jobs():
    session = db_session.create_session()
    all_jobs = session.query(Jobs).all()
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
                for item in all_jobs
            ]
        }
    )


@blueprint.route("/api/jobs/<job_id>", methods=["GET"])
def get_one_jobs(job_id):
    session = db_session.create_session()
    try:
        job = session.query(Jobs).get(int(job_id))
    except ValueError:
        return jsonify({"error": "Not found"})
    if not job:
        return jsonify({"error": "Not found"})
    return jsonify(
        {
            "jobs": job.to_dict(
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
