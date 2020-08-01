from flask import Blueprint, request, render_template, jsonify, current_app
from .models import Job, User
from .extensions import db
import jwt
from functools import wraps

main = Blueprint('main', __name__)


def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()

        invalid_msg = {
            'message': 'Invalid token. Registration and / or authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }

        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            user = User.query.filter_by(email=data['sub']).first()
            if not user:
                raise RuntimeError('User not found')
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401  # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401

    return _verify


def row2dict(row):
    return dict((col, getattr(row, col)) for col in row.__table__.columns.keys())


@main.route('/api/get-jobs', methods=["GET"])
def get_jobs():
    data = request.get_json()
    email = data["email"]
    employer = data['employer']
    if email is None and employer is None:
        all_jobs = Job.query.all()
    elif employer is not None:
        all_jobs = Job.query.filter_by(employer=employer).all()
    else:
        all_jobs = Job.query.filter_by(creator=email).all()

    wanted_jobs = [row2dict(job) for job in all_jobs]
    sort_criteria = data["sort"]
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
@token_required
def add_job(current_user):
    data = request.get_json()
    title = data["title"]
    positions = data["positions"]
    location = data["location"]
    description = data["description"]
    start = data["start-date"]
    end = data["end-date"]
    wage = data["wage"]
    employer = data["employer"]

    # Will Assign The Job To Account Who Created It
    email = jwt.decode(request.headers.get('Authorization', '').split()[1], current_app.config['SECRET_KEY'])['sub']

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
@token_required
def update_job(current_user):
    data = request.get_json()
    job_id = data['id']
    email = jwt.decode(request.headers.get('Authorization', '').split()[1], current_app.config['SECRET_KEY'])['sub']
    job = Job.query.filter_by(id=job_id, creator=email).first()
    if job:
        setattr(job, 'title', data['title'] or job.title)
        setattr(job, 'positions', data["positions"] or job.positions)
        setattr(job, 'date', data["date"] or job.date)
        setattr(job, 'start-date', data["start-date"] or job.start_date)
        setattr(job, 'end-date', data["end-date"] or job.end_date)
        setattr(job, 'location', data["location"] or job.location)
        setattr(job, 'description', data["description"] or job.description)
        setattr(job, 'wage', data["wage"] or job.wage)
        setattr(job, 'employer', data["employer"] or job.employer)
        db.session.commit()
    else:
        return "Not Authorized to Do This", 401
    return jsonify(
        id=job_id
    )


# Only Testing
@main.route('/api/update-job-page', methods=['GET'])
@token_required
def send_page():
    return render_template("testing_files/updatejob.html")


# Only Testing
@main.route("/api/successful_login")
def success():
    print("Success")
    return "Success Logging In"
