from flask import Blueprint
from .models import Job
from .extensions import db

main = Blueprint('main', __name__)


@main.route('/api/get-jobs', methods=["GET"])
def get_jobs():
    all_jobs = Job.query.all()
    return str(all_jobs)