from typing import Text

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

# from application.models import User
from application.models import Owner
from application.models import OwnerData
from application.database import db

import datetime

authowner = Blueprint('authowner', __name__)


@authowner.route('/loginowner', methods=['GET'])
def loginowner():
    return render_template('loginowner.html')


@authowner.route('/loginowner', methods=['POST'])
def login_postowner():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    # フォームの空欄を確認
    if email == '' or password == '':
        flash('メールアドレスまたはパスワードが空欄です')
        return redirect(url_for('authowner.loginowner'))

    # メールアドレスは 6 ~ 254 文字以内
    if not 6 <= len(email) <= 254:
        flash('メールアドレスは 6 ~ 254 文字以内にして下さい')
        return redirect(url_for('authowner.loginowner'))

    # パスワードの長さは 12 文字以上
    if not 7 <= len(password):
        flash('パスワードは 7 文字以上にして下さい')
        return redirect(url_for('authowner.loginowner'))

    user = Owner.query.filter_by(email=email).first()

    # ユーザ情報の有無を確認
    if not user:
        flash('入力されたメールアドレスが正しくありません')
        return redirect(url_for('authowner.loginowner'))

    # パスワードのチェック
    if not check_password_hash(user.password, password):
        flash('入力されたパスワードが正しくありません')
        return redirect(url_for('authowner.loginowner'))

    login_user(user, remember=remember)

    return redirect(url_for('authowner.home'))


@authowner.route('/signupowner', methods=['GET'])
def signupowner() -> Text:
    return render_template('signupowner.html')


@authowner.route('/signupowner', methods=['POST'])
def signup_postowner() -> Text:
    name = request.form.get('name')
    display_name = request.form.get('display_name')
    email = request.form.get('email')
    password = request.form.get('password')

    # フォームの空欄を確認
    if name == '' or display_name == '' or email == '' or password == '':
        flash('ユーザ名、表示名、メールアドレスまたはパスワードが空欄です')
        return redirect(url_for('authowner.signupowner'))

    # メールアドレスの重複を確認
    user_by_email = Owner.query.filter_by(email=email).first()
    if user_by_email:
        flash('このメールアドレスは既に使われています')
        return redirect(url_for('authowner.signupowner'))

    # ユーザ名の重複を確認
    user_by_name = Owner.query.filter_by(name=name).first()
    if user_by_name:
        flash('このユーザ名は既に使われています')
        return redirect(url_for('authowner.signupowner'))

    # ユーザ名は 2 ~ 15 文字以内
    if not 2 <= len(name) <= 15:
        flash('ユーザ名は 2 ~ 15 文字以内にして下さい')
        return redirect(url_for('authowner.signupowner'))

    # ユーザ名は英数字のみ
    if name.isalnum() is True:
        name = request.form.get('name').lower()
    else:
        flash('ユーザ名は英数字のみにして下さい')

    # 表示名は 50 文字以内
    if not 1 <= len(display_name) <= 50:
        flash('表示名は 50 文字以内にして下さい')
        return redirect(url_for('authowner.signupowner'))

    # メールアドレスは 6 ~ 254 文字以内
    if not 6 <= len(email) <= 254:
        flash('メールアドレスは 6 ~ 254 文字以内にして下さい')
        return redirect(url_for('authowner.signupowner'))

    # パスワードの長さは 12 文字以上
    if not 12 <= len(password):
        flash('パスワードは 12 文字以上にして下さい')
        return redirect(url_for('authowner.signupowner'))

    hashed_password = generate_password_hash(password, method='sha256')

    new_user = Owner(name=name, display_name=display_name, email=email, password=hashed_password, start_hour=9,start_minites=0,end_hour=20,end_minites=30)

    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    finally:
        db.session.close()

    return redirect(url_for('authowner.loginowner'))


@authowner.route('/logoutowner')
@login_required
def logoutowner() -> Text:
    logout_user()
    return redirect(url_for('main.index'))


@authowner.route('/home', methods=['GET'])
def home():
    if current_user.is_anonymous:
        flash('ログインをお願いします')
        return redirect(url_for('authowner.loginowner'))
    result = OwnerData.query.filter_by(name=current_user.name).all()
    owner_data = Owner.query.filter_by(name=current_user.name).first()
    return render_template('profileowner.html',name=current_user.display_name,owner=owner_data ,result=result)


@authowner.route('/home', methods=['POST'])
def home_post() -> Text:
    

    # name = request.form.get('name')
    name = current_user.name
    start_spot = request.form.get('start_spot')
    goal_spot = request.form.get('goal_spot')
    car_class = request.form.get('car_class')
    car_num = request.form.get('car_num')
    if car_num == None:
        car_num = ""
    child = request.form.get('child')
    if child == None:
        child = "なし"
    else:
        child = "あり"
    year = request.form.get('year')
    month = request.form.get('month')
    day = request.form.get('day')
    hour = request.form.get('hour')
    minites = request.form.get('minites')

    day_data = year + "-" + month + "-" + day + " " + hour + ":" + minites + ":00"
    return_date = datetime.datetime.strptime(day_data, '%Y-%m-%d %H:%M:%S')

    new_car = OwnerData(
        name=name,
        start_spot=start_spot,
        goal_spot=goal_spot,
        car_class=car_class,
        car_num=car_num,
        child=child,
        return_date=return_date,
        car_status=None,
        user_status="なし",
        user_name="なし",
        user_number="なし",
        user_mail="なし",
        user_check="なし")

    try:
        db.session.add(new_car)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    finally:
        db.session.close()


    return redirect(url_for('authowner.home'))

@authowner.route('/edit', methods=['GET'])
def edit():
    if current_user.is_anonymous:
        flash('ログインをお願いします')
        return redirect(url_for('authowner.loginowner'))

    search_id = request.args.get("id")
    result = OwnerData.query.filter_by(name=current_user.name,id=search_id).all()

    return render_template('editowner.html',name=current_user.name,result=result)


@authowner.route('/edit', methods=['POST'])
def edit_post() -> Text:

    search_id = request.args.get("id")

    # name = request.form.get('name')
    name = current_user.name
    start_spot = request.form.get('start_spot')
    goal_spot = request.form.get('goal_spot')
    car_class = request.form.get('car_class')
    car_num = request.form.get('car_num')
    car_status = request.form.get('car_status')
    if car_status == None:
        car_status = None
    else:
        car_status = "あり"
    if car_num == None:
        car_num = ""
    child = request.form.get('child')
    if child == None:
        child = "なし"
    else:
        child = "あり"
    return_date = request.form.get('return_date')

    update_car = OwnerData.query.filter_by(id=search_id).first()

    update_car.start_spot = start_spot
    update_car.goal_spot = goal_spot
    update_car.car_class = car_class
    update_car.car_num = car_num
    update_car.car_status = car_status
    update_car.child = child
    update_car.return_date = return_date

    try:
        db.session.add(update_car)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    finally:
        db.session.close()


@authowner.route('/data', methods=['GET'])
def car_data():
    if current_user.is_anonymous:
        flash('ログインをお願いします')
        return redirect(url_for('authowner.loginowner'))

    search_id = request.args.get("id")
    result = OwnerData.query.filter_by(id=search_id).all()

    return render_template('data.html',result=result)
