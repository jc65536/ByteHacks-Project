from flask import Blueprint, request, jsonify, current_app
from flask_cors import cross_origin
from .models import Job, User, Message
from .extensions import db
from . import YELP_API_KEY
import requests
from datetime import datetime
import jwt
from functools import wraps
import time

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
@cross_origin()
def get_jobs():
    data = request.args.to_dict()
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
        wanted_jobs = sorted(wanted_jobs, key=lambda job: datetime.fromisoformat(job['start_date']))
    # We might wanna implement this in the future
    # But that's only if we have like a standardized address system such that we can look up location
    elif sort_criteria == "location":
        pass
    elif sort_criteria == "wage":
        wanted_jobs = sorted(wanted_jobs, key=lambda job: job.wage, reverse=True)
    elif sort_criteria == "positions":
        wanted_jobs = sorted(wanted_jobs, key=lambda job: job.positions, reverse=True)

    return jsonify({ 'jobs': wanted_jobs })


@main.route('/api/add-job', methods=["POST"])
@cross_origin(supports_credentials=True)
@token_required
def add_job(current_user):
    data = request.get_json()
    title = get_data(data, "job")
    employer = get_data(data, "employer")
    positions = get_data(data, "positions")
    location = get_data(data, "location")
    description = get_data(data, "description")
    start = get_data(data, "start")
    end = get_data(data, "end")
    wage = get_data(data, "salary")

    # Will Assign The Job To Account Who Created It
    email = jwt.decode(request.headers.get('Authorization', '').split()[1], current_app.config['SECRET_KEY'])['sub']

    new_job = Job(title=title, positions=positions, location=location, description=description,
                  employer=employer, start_date=start, end_date=end, wage=wage, creator=email)

    db.session.add(new_job)
    db.session.commit()

    return jsonify(
        id=new_job.id
    )


@main.route("/api/update-job", methods=["POST"])
@cross_origin(supports_credentials=True)
@token_required
def update_job(current_user):
    data = request.get_json()
    job_id = get_data(data, "id")
    email = jwt.decode(request.headers.get('Authorization', '').split()[1], current_app.config['SECRET_KEY'])['sub']
    job = Job.query.filter_by(id=job_id, creator=email).first()
    if job:
        setattr(job, 'title', get_data(data, "title") or job.title)
        setattr(job, 'positions', get_data(data, "positions") or job.positions)
        setattr(job, 'date', get_data(data, "date") or job.date)
        setattr(job, 'start-date', get_data(data, "start-date") or job.start_date)
        setattr(job, 'end-date', get_data(data, "end-date") or job.end_date)
        setattr(job, 'location', get_data(data, "location") or job.location)
        setattr(job, 'description', get_data(data, "description") or job.description)
        setattr(job, 'wage', get_data(data, "wage") or job.wage)
        setattr(job, 'employer', get_data(data, "employer") or job.employer)
        db.session.commit()
    else:
        return "Not Authorized to Do This", 401
    return jsonify(
        id=job_id
    )


@main.route("/api/soup-info", methods=['GET'])
@cross_origin()
def get_info():
    data = request.args.to_dict()
    place_id = get_data(data, "id")
    if place_id:
        details_response = requests.get("https://api.yelp.com/v3/businesses/" + place_id,
                                        headers={"Authorization": "Bearer " + YELP_API_KEY})
        weekday = datetime.now().weekday()
        try:
            hours = details_response.json()["hours"][0]
            if (hours["is_open_now"]):
                return jsonify({"open": hours["open"][weekday]["start"], "close": hours["open"][weekday]["end"],
                                "open_now": True, "next_open": weekday, "successful": True})
            else:  # not open could be due to not open on that day or after closing hours
                # search for the next open day
                closed = True
                while closed:
                    weekday = (weekday + 1) % 7
                    for day in hours["open"]:
                        if day["day"] == weekday:
                            closed = False
                return jsonify({"open": hours["open"][weekday]["start"], "close": hours["open"][weekday]["end"],
                                "open_now": False, "next_open": weekday, "successful": True})
        except:  # no hours data
            return jsonify({'message': 'No hours data', "successful": False})
    else:
        return jsonify({'message': 'Need place ID', "successful": False}), 400

# yelp categories searched: employmentagencies, foodbanks, homelessshelters
@main.route("/api/soup", methods=["GET"])
@cross_origin()
def get_soup():
    data = request.args.to_dict()
    longitude = get_data(data, "longitude")
    latitude = get_data(data, "latitude")
    if (longitude is None) or (latitude is None):
        return jsonify({"message": "no location specified"}), 400
    radius = (get_data(data, "radius") or 5) * 1600  # miles to meters
    # Note the restriction in radius of https://www.yelp.com/developers/documentation/v3/business_search
    if radius >= 40000:
        return jsonify({"message": "radius too large - max is 25 miles"}), 400
    
    yelp_response = requests.get("https://api.yelp.com/v3/businesses/search",
                                 params={"longitude": longitude, "latitude": latitude, "radius": radius,
                                         "categories": "employmentagencies, foodbanks, homelessshelters"},
                                 headers={"Authorization": "Bearer " + YELP_API_KEY})
    businesses = yelp_response.json()["businesses"]

    class SimplifiedBusiness:
        def __init__(self, name, address, longitude, latitude, image, id):
            self.name = name
            self.address = address
            self.longitude = longitude
            self.latitude = latitude
            self.image = image
            self.id=id

    simplified_array = []
    for bus in businesses:
        simplified_array.append(SimplifiedBusiness(bus["name"], "".join(bus["location"]["display_address"]),
                                                   bus["coordinates"]["longitude"], bus["coordinates"]["latitude"],
                                                   bus["image_url"], bus["id"]).__dict__)

    return jsonify(simplified_array)


@main.route("/api/send-message", methods=["POST"])
@cross_origin(supports_credentials=True)
@token_required
def send_message(current_user):
    data = request.get_json()
    timestamp = time.time()
    sender_email = jwt.decode(request.headers.get('Authorization', '').split()[1], current_app.config['SECRET_KEY'])[
        'sub']
    try:
        recipient = data['recipient']
        message = data['message']
    except:
        return jsonify({'message': 'Invalid request', 'successful': False}), 400

    sender_user = User.query.filter_by(email=sender_email).first()

    recipient_user = User.query.filter_by(email=recipient).first()
    if recipient_user is None:
        return jsonify({'message': 'Recipient not found', 'successful': False}), 400

    msg = Message(author=sender_user, recipient=recipient_user, message=message, timestamp=timestamp)

    db.session.add(msg)
    db.session.commit()

    return jsonify({'message': 'Message sent successfully', 'successful': True})


@main.route("/api/get-message", methods=["GET"])
@cross_origin(supports_credentials=True)
@token_required
def recv_message(current_user):
    data = request.get_json()
    requestor_email = jwt.decode(request.headers.get('Authorization', '').split()[1], current_app.config['SECRET_KEY'])[
        'sub']

    requestor = User.query.filter_by(email=requestor_email).first()

    starting_time = 0
    if get_data(data, 'time'):
        starting_time = time

    recieved_messages = [{'timestamp': message.timestamp, 'sender_email': User.query(id=message.sender_id),
                          'reciever_email': User.query(id=message.recipient_id), 'message': message.message} for message
                         in
                         requestor.messages_recieved.filter(
                             Message.timestamp >= starting_time
                         ).all()]

    sent_messages = [{'timestamp': message.timestamp, 'sender_email': User.query(id=message.sender_id),
                      'reciever_email': User.query(id=message.recipient_id), 'message': message.message} for message in
                     requestor.messages_sent.filter(
                         Message.timestamp >= starting_time
                     ).all()]

    all_messages = sorted(recieved_messages + sent_messages, key=lambda i: i['timestamp'])

    return jsonify(all_messages)
