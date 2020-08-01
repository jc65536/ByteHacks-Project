from flask import Blueprint, request, render_template, jsonify
from flask_login import current_user, login_required
from .models import Job
from .extensions import db
import json

main = Blueprint('main', __name__)

def row2dict(row):
    return dict((col, getattr(row, col)) for col in row.__table__.columns.keys())

@main.route('/api/get-jobs', methods=["GET"])
def get_jobs():
    employer_id = request.form.get("employer")
    if employer_id is None:
        all_jobs = Job.query.all()
    else:
        all_jobs = Job.query.filter(Job.employer == employer_id)

    sort_criteria = request.form.get("sort")
    if sort_criteria == "date" or sort_criteria is None:        # if variable "sort" doesn't exist it returns None right?
        pass
    elif sort_criteria == "location":
        pass
    elif sort_criteria == "wage":
        all_jobs = sorted(all_jobs, key=lambda job: job.wage, reverse=True)
    elif sort_criteria == "positions":
        all_jobs = sorted(all_jobs, key=lambda job: job.positions, reverse=True)

    return jsonify([row2dict(job) for job in all_jobs])


@main.route('/api/add-job', methods=["POST"])
@login_required
def add_job():
    title = request.form.get("title")
    positions = request.form.get("positions")
    date = request.form.get("date")
    location = request.form.get("location")
    description = request.form.get("description")
    duration = request.form.get("duration")
    wage = request.form.get("wage")

    # Will Assign The Job To Employer
    employer_uname = current_user.username

    new_job = Job(title=title, positions=positions, date=date, location=location, description=description,
                  employer=employer_uname, duration=duration, wage=wage)

    db.session.add(new_job)
    db.session.commit()

    return jsonify(
        id=new_job.id
    )

@main.route('/api/add-job-page', methods=["GET"])
def show_page():
    return render_template("testing_files/addjob.html")

@main.route("/api/update-job", methods=["POST"])
@login_required
def update_job():
    job_id = request.form.get("id")
    job = Job.query.filter_by(id=job_id, employer=current_user.username)
    if job:
        setattr(job, title, request.form.get("title") or job.title)
        setattr(job, positions, request.form.get("positions") or job.positions)
        setattr(job, date, request.form.get("date") or job.date)
        setattr(job, duration, request.form.get("duration") or job.duration)
        setattr(job, location, request.form.get("location") or job.location)
        setattr(job, description, request.form.get("description") or job.description)
        setattr(job, wage, request.form.get("wage") or job.wage)
        db.session.commit()


# Only Testing
@main.route("/api/successful_login")
def success():
    print("Succ")
    return "Success Logging In"
