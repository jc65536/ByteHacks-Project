from flask import Blueprint, request, render_template, jsonify, make_response
from flask_login import current_user, login_required
from .models import Job
from .extensions import db
import json

main = Blueprint('main', __name__)


def row2dict(row):
    return dict((col, getattr(row, col)) for col in row.__table__.columns.keys())


@main.route('/api/get-jobs', methods=["GET"])
def get_jobs():
    email = request.args.get("email")
    employer = request.args.get('employer')
    if email is None and employer is None:
        all_jobs = Job.query.all()
    elif employer is not None:
        all_jobs = Job.query.filter_by(employer=employer).all()
    else:
        all_jobs = Job.query.filter_by(creator=email).all()

    wanted_jobs = [row2dict(job) for job in all_jobs]
    sort_criteria = request.form.get("sort")
    if sort_criteria == "date" or sort_criteria is None:
        wanted_jobs = sorted(wanted_jobs, key=lambda job: job.date, reverse=True)
    # We might wanna implement this in the future
    # But that's only if we have like a standardized address system such that we can look up location
    elif sort_criteria == "location":
        pass
    elif sort_criteria == "wage":
        wanted_jobs = sorted(wanted_jobs, key=lambda job: job.wage, reverse=True)
    elif sort_criteria == "positions":
        wanted_jobs = sorted(wanted_jobs, key=lambda job: job.positions, reverse=True)

    return jsonify(wanted_jobs)


@main.route('/api/add-job', methods=["POST"])
@login_required
def add_job():
    title = request.form.get("title")
    positions = request.form.get("positions")
    location = request.form.get("location")
    description = request.form.get("description")
    start = request.form.get("start-date")
    end = request.form.get("end-date")
    wage = request.form.get("wage")
    employer = request.form.get("employer")

    # Will Assign The Job To Account Who Created It
    email = current_user.email

    new_job = Job(title=title, positions=positions, location=location, description=description,
                  employer=employer, start_date=start, end_date=end, wage=wage, creator=email)

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
    print(job_id)
    job = Job.query.filter_by(id=job_id, creator=current_user.email).first()
    print(job)
    if job:
        setattr(job, 'title', request.form.get("title") or job.title)
        setattr(job, 'positions', request.form.get("positions") or job.positions)
        setattr(job, 'date', request.form.get("date") or job.date)
        setattr(job, 'start-date', request.form.get("start-date") or job.start_date)
        setattr(job, 'end-date', request.form.get("end-date") or job.end_date)
        setattr(job, 'location', request.form.get("location") or job.location)
        setattr(job, 'description', request.form.get("description") or job.description)
        setattr(job, 'wage', request.form.get("wage") or job.wage)
        setattr(job, 'employer', request.form.get("employer") or job.employer)
        db.session.commit()
    else:
        return "Not Authorized to Do This", 401
    return jsonify(
        id=job_id
    )


# Only Testing
@main.route('/api/update-job-page', methods=['GET'])
@login_required
def send_page():
    return render_template("testing_files/updatejob.html")


# Only Testing
@main.route("/api/successful_login")
def success():
    print("Success")
    return "Success Logging In"
