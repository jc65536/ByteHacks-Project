from flask import Blueprint, request, render_template, jsonify, current_app
from flask_cors import cross_origin
from .models import Job, User
from .extensions import db
import json
import requests
from datetime import datetime
import jwt
from functools import wraps

main = Blueprint('main', __name__)

def get_data(data, property):
    try:
        return data[property]
    except:
        return None

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
    email = get_data(data, "email")
    employer = get_data(data, 'employer')
    if email is None and employer is None:
        all_jobs = Job.query.all()
    elif employer is not None:
        all_jobs = Job.query.filter_by(employer=employer).all()
    else:
        all_jobs = Job.query.filter_by(creator=email).all()

    wanted_jobs = [row2dict(job) for job in all_jobs]
    sort_criteria = get_data(data, "sort")
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
    title = get_data(data, "title")
    positions = get_data(data, "positions")
    location = get_data(data, "location")
    description = get_data(data, "description")
    start = get_data(data, "start-date")
    end = get_data(data, "end-date")
    wage = get_data(data, "wage")
    employer = get_data(data, "employer")

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
    job_id = get_data(data, "id")
    email = jwt.decode(request.headers.get('Authorization', '').split()[1], current_app.config['SECRET_KEY'])['sub']
    job = Job.query.filter_by(id=job_id, creator=current_user.email).first()
    if job:
        setattr(job, 'title', data["title"] or job.title)
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

# yelp categories searched: employmentagencies, foodbanks, homelessshelters
@main.route("/api/soup", methods=["GET"])
def get_soup():
    data = request.get_json(force=True)
    secret_file = open("yelpsecrets", "r")
    yelp_id = secret_file.readline()
    yelp_key = secret_file.readline().strip("\n")

    place_id = get_data(data, "id")
    if not(place_id is None):
        details_response = requests.get("https://api.yelp.com/v3/businesses/" + place_id, headers={"Authorization": "Bearer " + yelp_key})
        weekday = datetime.now().weekday()
        try:
            hours = details_response.json()["hours"][0]
            if (hours["is_open_now"]):
                return {"open": hours["open"][weekday]["start"], "close": hours["open"][weekday]["end"], "open_now": True, "next_open": weekday}
            else:           # not open could be due to not open on that day or after closing hours
                # search for the next open day
                closed = True
                while closed:
                    weekday = (weekday + 1) % 7
                    for day in hours["open"]:
                        if day["day"] == weekday:
                            closed = False
                return {"open": hours["open"][weekday]["start"], "close": hours["open"][weekday]["end"], "open_now": False, "next_open": weekday}
        except:         # no hours data
            return "No hours data for this place."
    
    longitude = get_data(data, "longitude")
    latitude = get_data(data, "latitude")
    if ((longitude is None) or (latitude is None)):
        return "Error: no location", 404
    radius = (data["radius"] or 5) * 1600           # miles to meters

    yelp_response = requests.get("https://api.yelp.com/v3/businesses/search", params={"longitude": longitude, "latitude": latitude, "radius": radius, "categories": "employmentagencies, foodbanks, homelessshelters"}, headers={"Authorization": "Bearer " + yelp_key})
    businesses = yelp_response.json()["businesses"]

    class SimplifiedBusiness:
        def __init__(self, name, address, longitude, latitude, image):
            self.name = name; self.address = address; self.longitude = longitude; self.latitude = latitude; self.image = image

    simplified_array = []
    for bus in businesses:
        simplified_array.append(SimplifiedBusiness(bus["name"], "".join(bus["location"]["display_address"]), bus["coordinates"]["longitude"], bus["coordinates"]["latitude"], bus["image_url"]).__dict__)

    return json.dumps(simplified_array)


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
