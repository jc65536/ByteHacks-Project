from flask import Blueprint, request, jsonify, current_app
from flask_cors import cross_origin
from .models import Job, User, Message
from .extensions import db
from . import YELP_API_KEY
import requests
from datetime import datetime
import dateutil.parser
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
    jobid = get_data(data, 'id')
    if email:
        all_jobs = Job.query.filter_by(creator=email).all()
    elif employer:
        all_jobs = Job.query.filter_by(employer=employer).all()
    elif jobid:
        all_jobs = Job.query.filter_by(id=jobid).all()
    else:
        all_jobs = Job.query.all()

    def dateSort(job):
        return dateutil.parser.isoparse(job['start_date'])
        ## might need to add more error handling

    wanted_jobs = [row2dict(job) for job in all_jobs]
    sort_criteria = get_data(data, "sort")
    if sort_criteria == "date" or sort_criteria is None:
        wanted_jobs = sorted(wanted_jobs, key=dateSort)
    elif sort_criteria == "positions":
        wanted_jobs = sorted(wanted_jobs, key=lambda job: job.positions, reverse=True)

    return jsonify({'jobs': wanted_jobs})


@main.route('/api/add-job', methods=["POST"])
@cross_origin(supports_credentials=True)
@token_required
def add_job(current_user):
    data = request.get_json()
    title = get_data(data, "title")
    employer = get_data(data, "employer")
    positions = get_data(data, "positions")
    location = get_data(data, "location")
    description = get_data(data, "description")
    start = get_data(data, "start_date")
    end = get_data(data, "end_date")
    wage = get_data(data, "wage")

    if (title is None or employer is None or positions is None or location is None or description is None or start is None or end is None or wage is None):
        return "Fields are missing!", 400

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
    delete = get_data(data, "delete")
    email = jwt.decode(request.headers.get('Authorization', '').split()[1], current_app.config['SECRET_KEY'])['sub']
    job = Job.query.filter_by(id=job_id, creator=email).first()
    if job and delete:
        db.session.delete(job)
        db.session.commit()
    elif job:
        setattr(job, 'title', get_data(data, "title") or job.title)
        setattr(job, 'positions', get_data(data, "positions") or job.positions)
        setattr(job, 'start-date', get_data(data, "start_date") or job.start_date)
        setattr(job, 'end-date', get_data(data, "end_date") or job.end_date)
        setattr(job, 'location', get_data(data, "location") or job.location)
        setattr(job, 'description', get_data(data, "description") or job.description)
        setattr(job, 'wage', get_data(data, "wage") or job.wage)
        setattr(job, 'employer', get_data(data, "employer") or job.employer)
        db.session.commit()
    else:
        return "Not Authorized to Do This", 401
    return jsonify({
        'id': job_id,
        'success': True
    })


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
                i = 0
                while i < 7:
                    i += 1
                    for day in hours["open"]:
                        if day["day"] == weekday:
                            return jsonify(
                                {"open": hours["open"][weekday]["start"], "close": hours["open"][weekday]["end"],
                                 "open_now": False, "next_open": weekday, "successful": True})
                    weekday = (weekday + 1) % 7
                return jsonify({'message': 'No hours data', "successful": False})
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
    radius = int(get_data(data, "radius") or 5) * 1600  # miles to meters
    # Note the restriction in radius of https://www.yelp.com/developers/documentation/v3/business_search
    if radius > 40000:
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
            self.id = id

    simplified_array = []
    for bus in businesses:
        simplified_array.append(SimplifiedBusiness(bus["name"], " ".join(bus["location"]["display_address"]),
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
        subject = data['subject']
        jobid = data['jobid']
    except:
        return jsonify({'message': 'Invalid request', 'successful': False}), 400

    sender_user = User.query.filter_by(email=sender_email).first()

    recipient_user = User.query.filter_by(email=recipient).first()
    if recipient_user is None:
        return jsonify({'message': 'Recipient not found', 'successful': False}), 400

    msg = Message(author=sender_user, recipient=recipient_user, message=message, subject=subject, jobid=jobid, timestamp=timestamp)

    db.session.add(msg)
    db.session.commit()

    return jsonify({'message': 'Message sent successfully', 'successful': True})


@main.route("/api/get-messages", methods=["GET"])
@cross_origin(supports_credentials=True)
@token_required
def recv_message(current_user):
    data = request.args.to_dict()

    requestor = current_user

    starting_time = 0
    if get_data(data, 'time'):
        starting_time = get_data(data, 'time')

    received_messages = [{'timestamp': message.timestamp, 'sender_email': User.query.filter_by(id=message.sender_id).first().email,
                          'receiver_email': requestor.email, 'message': message.message, 'subject': message.subject, 'jobid': message.jobid, 'id': message.id} 
                          for message in
                         requestor.messages_received.filter(
                             Message.timestamp >= starting_time
                         ).all()]

    sent_messages = [{'timestamp': message.timestamp, 'sender_email': requestor.email, 'receiver_email': User.query.filter_by(id=message.recipient_id).first().email, 
                    'message': message.message, 'subject': message.subject, 'jobid': message.jobid, 'id': message.id} 
                      for message in
                     requestor.messages_sent.filter(
                         Message.timestamp >= starting_time
                     ).all()]

    received_messages = sorted(received_messages, key=lambda i: i['timestamp'], reverse=True)
    sent_messages = sorted(sent_messages, key=lambda i: i['timestamp'], reverse=True)
    all_messages = sorted(sent_messages + received_messages, key=lambda i: i['timestamp'], reverse=True)

    return jsonify({'received': received_messages, 'sent': sent_messages, 'all_messages': all_messages})

@main.route("/api/accept-application", methods=["POST"])
@cross_origin(supports_credentials=True)
@token_required
def accept_application(current_user):
    data = request.get_json()

    try:
        message_id = data['message_id']
    except:
        return jsonify({'message': 'Invalid request', 'successful': False}), 400

    msg = Message.query.filter_by(id=message_id).first()
    job = Job.query.filter_by(id=msg.jobid).first()

    if not (msg.subject.startswith('APPLICATION') and msg.recipient_id == current_user.id and job.creator == current_user.email):
        return jsonify({'message': 'Not authorized', 'successful': False}), 401

    
    db.session.delete(msg)
    job.positions = job.positions - 1
    if job.positions == -1:
        job.positions = 0

    db.session.commit()

    return jsonify({'message': 'Application closed', 'successful': True})