from flask import Blueprint

main = Blueprint('main', __name__)


@main.route('/api/add-job', methods=["POST"])
def add_job():
