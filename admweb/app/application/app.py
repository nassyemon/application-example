from flask import Blueprint, render_template,request,redirect, url_for,flash,current_app
from flask_login import current_user

from application.models import OwnerData
from application.database import db
import datetime


app = Blueprint('main', __name__)

@app.before_request
def before_request():
    print(current_app.env)
    # if not request.is_secure and current_app.env != 'development':
    #     url = request.url.replace('http://', 'https://', 1)
    #     code = 301
    #     return redirect(url, code=code)

@app.route('/')
def index():
    print(current_user.is_anonymous)
    print("------------")
    print("あああああああ")
    dt_now = datetime.datetime.now()
    # result = OwnerData.query.order_by(OwnerData.return_date.desc()).filter(OwnerData.return_date > dt_now).filter_by(car_status=None,display_status=None,user_status="なし").all()
    result = OwnerData.query.order_by(OwnerData.return_date.desc()).filter_by(car_status="予約可",display_status=None,user_status="なし").all()
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

    start_date = request.form.get('start_date')
    return_date = request.form.get('return_date')

    print(request.form)
    

    if len(start_spot) > 0 and len(goal_spot) == 0:
        result = OwnerData.query.filter(OwnerData.start_spot.like(search_start_spot)).filter_by(car_status=None)
    elif len(start_spot) == 0 and len(goal_spot) > 0:
        result = OwnerData.query.filter(OwnerData.goal_spot.like(search_goal_spot)).filter_by(car_status=None)
    else:
        result = OwnerData.query.filter(OwnerData.start_spot.like(search_start_spot),OwnerData.goal_spot.like(search_goal_spot)).filter_by(car_status=None)

    if len(start_date) > 0:
        result = result.filter(OwnerData.return_date >= start_date)

    if len(return_date) > 0:
        result = result.filter(OwnerData.return_date <= return_date)
    return render_template('search_result.html',result=result.all())


@app.route('/show', methods=['GET', 'POST'])
def show():
    search_id = request.args.get("id")

    result = OwnerData.query.filter_by(id=search_id).all()
    return render_template('show.html', result=result, user=current_user)


@app.route('/service', methods=['GET', 'POST'])
def service():
    return render_template('service.html')

@app.route('/privacy', methods=['GET', 'POST'])
def privacy():
    return render_template('privacy.html')

@app.route('/law', methods=['GET', 'POST'])
def law():
    return render_template('law.html')
