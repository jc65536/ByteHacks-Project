from flask import Blueprint, request
from flask_login import current_user, login_required
from .models import Job
from .extensions import db
import json

main = Blueprint('main', __name__)


@main.route('/api/get-jobs', methods=["GET"])
def get_jobs():
    all_jobs = Job.query.all()

    sort_criteria = request.form.get("sort")
    if sort_criteria == "date" or sort_criteria == None:        # if variable "sort" doesn't exist it returns None right?
        pass
    elif sort_criteria == "location":
        pass
    elif sort_criteria == "wage":
        all_jobs = sorted(all_jobs, key=lambda job: job.wage, reverse=True)
    elif sort_criteria == "positions":
        all_jobs = sorted(all_jobs, key=lambda job: job.positions, reverse=True)

    json_string = json.dumps(all_jobs, default=lambda job: job.__dict__())
    return json_string

@main.route('/api/add-job', methods=["POST"])
@login_required
def add_job():
    title = request.form.get("title")
    positions = request.form.get("positions")
    date = request.form.get("date")
    location = request.form.get("location")
    description = request.form.get("description")

    # Will Assign The Job To Employer
    employer_uname = current_user.username

    new_job = Job(title=title, positions=positions, date=date, location=location, description=description, employer=employer_uname)

    db.session.add(new_job)
    db.session.commit()

    return new_job.id
