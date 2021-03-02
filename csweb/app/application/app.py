from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, session
from flask_login import current_user

from application.models import OwnerData
from application.database import db
import datetime


app = Blueprint('main', __name__)

# @app.before_request
# def before_request():
#     if not request.is_secure and current_app.env != 'development':
#         url = request.url.replace('http://', 'https://', 1)
#         code = 301
#         return redirect(url, code=code)

@app.route('/')
def index():
    dt_now = datetime.datetime.now()
    # result = OwnerData.query.order_by(OwnerData.return_date.desc()).filter(OwnerData.return_date > dt_now).filter_by(car_status='予約可',display_status=None,user_status="なし").all()
    result = OwnerData.query.order_by(OwnerData.return_date.desc()).all()
    return render_template('index.html', result = result)

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/result', methods=['POST'])
def search_result():
    start_spot = request.form.get('start_spot')
    goal_spot = request.form.get('goal_spot')
    search_start_spot = "%{}%".format(start_spot)
    search_goal_spot = "%{}%".format(goal_spot)

    take_day = request.form.get('take_day')
    return_day = request.form.get('return_day')
    take_time = request.form.get('take_time')
    return_time = str(request.form.get('return_time'))

    if len(start_spot) > 0 and len(goal_spot) == 0:
        result = OwnerData.query.filter(OwnerData.start_spot.like(search_start_spot)).filter_by(car_status=None)
    elif len(start_spot) == 0 and len(goal_spot) > 0:
        result = OwnerData.query.filter(OwnerData.goal_spot.like(search_goal_spot)).filter_by(car_status=None)
    else:
        result = OwnerData.query.filter(OwnerData.start_spot.like(search_start_spot),OwnerData.goal_spot.like(search_goal_spot)).filter_by(car_status=None)

    if len(take_day) > 0 and len(take_time) > 0:
        take_date = take_day + " " + take_time + ":00"
        take_date = datetime.datetime.strptime(take_date,'%Y-%m-%d %H:%M:%S')
        result = result.filter(OwnerData.return_date >= take_date)

    if len(return_day) > 0 and len(return_time) > 0:
        return_date = return_day + " " + return_time + ":00"
        return_date = datetime.datetime.strptime(return_date,'%Y-%m-%d %H:%M:%S')
        result = result.filter(OwnerData.return_date >= return_date)
    return render_template('search_result.html',result=result.all())


@app.route('/show', methods=['GET', 'POST'])
def show():
    search_id = request.args.get("id")

    result = OwnerData.query.filter_by(id=search_id).first()
    display_day = result.display_date.date()
    return_day = result.return_date.date()
    return render_template('show.html', res=result, user=current_user, display_day=display_day, return_day=return_day)


@app.route('/service', methods=['GET', 'POST'])
def service():
    return render_template('service.html')

@app.route('/privacy', methods=['GET', 'POST'])
def privacy():
    return render_template('privacy.html')

@app.route('/law', methods=['GET', 'POST'])
def law():
    return render_template('law.html')