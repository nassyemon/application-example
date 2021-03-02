from typing import Text

from flask import Blueprint, render_template, redirect, url_for, request, flash,make_response,current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

from application.models import User
from application.models import Owner
from application.models import OwnerData
from application.database import db

import datetime
from io import StringIO
import csv

from . import user_mail


auth = Blueprint('auth', __name__)

@auth.before_request
def before_request():
    print(current_app.env)
    # if not request.is_secure and current_app.env != 'development':
    #     url = request.url.replace('http://', 'https://', 1)
    #     code = 301
    #     return redirect(url, code=code)


@auth.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    # フォームの空欄を確認
    if email == '' or password == '':
        flash('メールアドレスまたはパスワードが空欄です')
        return redirect(url_for('auth.login'))

    # メールアドレスは 6 ~ 254 文字以内
    if not 6 <= len(email) <= 254:
        flash('メールアドレスは 6 ~ 254 文字以内にして下さい')
        return redirect(url_for('auth.login'))

    # パスワードの長さは 7 文字以上
    if not 7 <= len(password):
        flash('パスワードは 7 文字以上にして下さい')
        return redirect(url_for('auth.login'))

    user = Owner.query.filter_by(email=email).first()

    # ユーザ情報の有無を確認
    if not user:
        flash('入力されたメールアドレスが正しくありません')
        return redirect(url_for('auth.login'))

    # パスワードのチェック
    if not check_password_hash(user.password, password):
        flash('入力されたパスワードが正しくありません')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)

    # owner_master = Owner.query.filter_by(email=email).first()
    # owner_master.master = True
    # try:
    #     db.session.add(owner_master)
    #     db.session.commit()
    # except Exception:
    #     db.session.rollback()
    #     raise
    # finally:
    #     db.session.close()

    return redirect(url_for('auth.profile'))


@auth.route('/signup', methods=['GET'])
def signup() -> Text:
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post() -> Text:
    name = request.form.get('name')
    display_name = request.form.get('display_name')
    email = request.form.get('email')
    password = request.form.get('password')

    # フォームの空欄を確認
    if name == '' or display_name == '' or email == '' or password == '':
        flash('ユーザ名、表示名、メールアドレスまたはパスワードが空欄です')
        return redirect(url_for('auth.signup'))

    # メールアドレスの重複を確認
    user_by_email = Owner.query.filter_by(email=email).first()
    if user_by_email:
        flash('このメールアドレスは既に使われています')
        return redirect(url_for('auth.signup'))

    # ユーザ名の重複を確認
    user_by_name = Owner.query.filter_by(name=name).first()
    if user_by_name:
        flash('このユーザ名は既に使われています')
        return redirect(url_for('auth.signup'))

    # ユーザ名は 2 ~ 7 文字以内
    if not 2 <= len(name) <= 15:
        flash('ユーザ名は 2 ~ 15 文字以内にして下さい')
        return redirect(url_for('auth.signup'))

    # ユーザ名は英数字のみ
    if name.isalnum() is True:
        name = request.form.get('name').lower()
    else:
        flash('ユーザ名は英数字のみにして下さい')
        return redirect(url_for('auth.signup'))

    # 表示名は 50 文字以内
    if not 1 <= len(display_name) <= 50:
        flash('表示名は 50 文字以内にして下さい')
        return redirect(url_for('auth.signup'))

    # メールアドレスは 6 ~ 254 文字以内
    if not 6 <= len(email) <= 254:
        flash('メールアドレスは 6 ~ 254 文字以内にして下さい')
        return redirect(url_for('auth.signup'))

    # パスワードの長さは 7 文字以上
    if not 7 <= len(password):
        flash('パスワードは 7 文字以上にして下さい')
        return redirect(url_for('auth.signup'))

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

    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout() -> Text:
    logout_user()
    return redirect(url_for('main.index'))




@auth.route('/adduser', methods=['GET'])
def adduser():
    search_id = request.args.get("id")
    user_get_day = request.args.get("user_get_day")
    user_get_time = request.args.get("user_get_time")
    user_return_day = request.args.get("user_return_day")
    user_return_time = request.args.get("user_return_time")

    user_get_datetime = user_get_day + " " + user_get_time + ":00"
    user_return_datetime = user_return_day + " " + user_return_time + ":00"
    user_get_datetime = datetime.datetime.strptime(user_get_datetime,'%Y-%m-%d %H:%M:%S')
    user_return_datetime = datetime.datetime.strptime(user_return_datetime,'%Y-%m-%d %H:%M:%S')


    if not search_id == None:
        resister_car = OwnerData.query.filter_by(id=search_id).first()
        print("ああああああああああ")
        print(user_return_datetime)
        print("いいいいいいいいい")
        print(resister_car.return_date)
        resister_car.user_mail = current_user.email
        resister_car.user_name = current_user.name
        resister_car.user_status = "あり"
        # resister_car.user_return_day = user_return_datetime
        resister_car.user_return_date = user_return_datetime
        resister_car.user_take_date = user_get_datetime
        print(resister_car.user_return_date)
        # resister_car.user_number = current_user.
        resister_car.user_check = '予約あり'
        try:
            db.session.add(resister_car)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
        finally:
            db.session.close()
    return redirect(url_for('auth.profile'))

@auth.route('/profile', methods=['GET'])
def profile():
    if current_user.is_anonymous:
        flash('ログインをお願いします')
        return redirect(url_for('auth.login'))
    if current_user.master:
        result = OwnerData.query.order_by(OwnerData.updated_at.desc()).all()
    else:
        result = OwnerData.query.filter_by(name=current_user.name,owner_delete_status=None).order_by(OwnerData.updated_at.desc()).all()
    owner_data = Owner.query.filter_by(name=current_user.name).first()
    return render_template('profileowner.html',name=current_user.display_name,owner=owner_data ,result=result)

@auth.route('/profile', methods=['POST'])
def profile_post() -> Text:

    name = current_user.name
    start_spot = request.form.get('start_spot')
    goal_spot = request.form.get('goal_spot')
    car_class = request.form.get('car_class')
    car_num = request.form.get('car_num')
    child = request.form.get('child')
    remarks = request.form.get('remarks')
    if car_num == None:
        car_num = ""

    nosmoke = request.form.get('option1')
    wd4 = request.form.get('option2')
    studless = request.form.get('option3')

    car_status = request.form.get('car_status')

    if car_status == None:
        car_status = "予約不可"

    if not nosmoke == None:
        nosmoke = True
    if not wd4 == None:
        wd4 = True
    if not studless == None:
        studless = True

    display_day = request.form.get('display_day')
    return_day = request.form.get('return_day')
    display_time = str(request.form.get('display_time'))
    return_time = str(request.form.get('return_time'))

    return_date = return_day + " " + return_time + ":00"
    return_date = datetime.datetime.strptime(return_date,'%Y-%m-%d %H:%M:%S')

    display_date = display_day + " " + display_time + ":00"
    display_date = datetime.datetime.strptime(display_date,'%Y-%m-%d %H:%M:%S')

    # server mode
    # return_date = datetime.datetime.strptime(return_date, '%Y-%m-%dT%H:%M')
    # display_date = datetime.datetime.strptime(display_date, '%Y-%m-%dT%H:%M')
    

    new_car = OwnerData(
        name=name,
        start_spot=start_spot,
        goal_spot=goal_spot,
        car_class=car_class,
        car_num=car_num,
        child=child,
        nosmoke=nosmoke,
        wd4=wd4,
        studless=studless,
        return_date=return_date,
        remarks=remarks,
        display_status=None,
        car_status=car_status,
        owner_delete_status=None,
        display_date=display_date,
        user_take_date=None,
        user_return_date=None,
        user_status="なし",
        user_name="なし",
        user_number="なし",
        user_mail="なし",
        user_check="なし",
        user_price=0,
        user_remarks="なし",
        updated_at=datetime.datetime.now())

    try:
        db.session.add(new_car)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    finally:
        db.session.close()


    return redirect(url_for('auth.profile'))

@auth.route('/cancel')
def car_cancel():
    if current_user.is_anonymous:
        flash('ログインをお願いします')
        return redirect(url_for('auth.login'))

    search_id = request.args.get("id")
    resister_car = OwnerData.query.filter_by(id=search_id).first()
    resister_car.user_mail = None
    resister_car.user_name = None
    resister_car.user_status = "なし"
    resister_car.user_day = None
    try:
        db.session.add(resister_car)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    finally:
        db.session.close()
    return redirect(url_for('auth.profile'))


@auth.route('/edit', methods=['GET'])
def edit():
    if current_user.is_anonymous:
        flash('ログインをお願いします')
        return redirect(url_for('auth.login'))

    search_id = request.args.get("id")
    result = OwnerData.query.filter_by(name=current_user.name,id=search_id).first()

    result.return_date = datetime.datetime.strftime(result.return_date,'%Y-%m-%dT%H:%M:%S')
    result.display_date = datetime.datetime.strftime(result.display_date,'%Y-%m-%dT%H:%M:%S')

    return render_template('editowner.html',name=current_user.name,res=result)


@auth.route('/edit', methods=['POST'])
def edit_post() -> Text:

    search_id = request.args.get("id")

    # name = request.form.get('name')
    name = current_user.name
    start_spot = request.form.get('start_spot')
    goal_spot = request.form.get('goal_spot')
    car_class = request.form.get('car_class')
    car_num = request.form.get('car_num')
    car_status = request.form.get('car_status')
    child = request.form.get('child')
    return_date = request.form.get('return_date')
    display_date = request.form.get('display_date')

    update_car = OwnerData.query.filter_by(id=search_id).first()

    update_car.start_spot = start_spot
    update_car.goal_spot = goal_spot
    update_car.car_class = car_class
    update_car.car_num = car_num
    update_car.car_status = car_status
    update_car.child = child
    update_car.return_date = return_date
    update_car.display_date = display_date

    try:
        db.session.add(update_car)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    finally:
        db.session.close()
    return redirect(url_for('auth.profile'))
    


@auth.route('/data', methods=['GET'])
def car_data():
    if current_user.is_anonymous:
        flash('ログインをお願いします')
        return redirect(url_for('auth.login'))

    search_id = request.args.get("id")
    result = OwnerData.query.filter_by(id=search_id).all()

    return render_template('data.html',result=result)

@auth.route('/delete', methods=['GET'])
def car_delete ():
    if current_user.is_anonymous:
        flash('ログインをお願いします')
        return redirect(url_for('auth.login'))

    search_id = request.args.get("id")
    result = OwnerData.query.filter_by(id=search_id).first()

    result.car_status = "予約不可"
    print(result.owner_delete_status)
    result.owner_delete_status = "削除"
    print(result.owner_delete_status)

    try:
        db.session.add(result)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    finally:
        db.session.close()

    return redirect(url_for('auth.profile'))

@auth.route('/rental', methods=['GET'])
def car_rental ():
    if current_user.is_anonymous:
        flash('ログインをお願いします')
        return redirect(url_for('auth.login'))

    search_id = request.args.get("id")
    result = OwnerData.query.filter_by(id=search_id).first()

    result.user_check = "貸出中"

    try:
        db.session.add(result)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    finally:
        db.session.close()

    return redirect(url_for('auth.profile'))

@auth.route('/payment', methods=['GET'])
def car_payment ():
    if current_user.is_anonymous:
        flash('ログインをお願いします')
        return redirect(url_for('auth.login'))

    search_id = request.args.get("id")
    result = OwnerData.query.filter_by(id=search_id).first()

    result.user_check = "支払い済"

    try:
        db.session.add(result)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    finally:
        db.session.close()

    return redirect(url_for('auth.profile'))

@auth.route('/download')
def download():
    search_id = request.args.get("mail")

    user_mail.send_csv_data()

    dt_now = datetime.datetime.now()

    # item_columns = OwnerData.query.filter_by(name=current_user.name).first()
    item_columns = OwnerData.query.filter(OwnerData.return_date > dt_now).filter_by(user_check="予約あり").all()
    f = StringIO()
    writer = csv.writer(f, quotechar='"', quoting=csv.QUOTE_ALL, lineterminator="\n")

    writer.writerow(['id','店舗名','出発地点','到着地点','車両クラス','車両ナンバー','返却期限日','ユーザーネーム','電話番号','メールアドレス','受け取り時間','返却時間','値段','ユーザー要望'])
    for data in item_columns:
        if data.user_number == None:
            user_number = '000-0000-0000'
        else:
            user_number = data.user_number
        print(data)
        writer.writerow([
            data.id,
            data.name,
            data.start_spot,
            data.goal_spot,
            data.car_class,
            data.car_num,
            data.return_date,
            data.user_name,
            user_number,
            data.user_mail,
            data.user_take_date,
            data.user_return_date,
            data.user_price,
            data.user_remarks
        ])

    res = make_response()
    res.data = f.getvalue()
    res.headers['Content-Type'] = 'text/csv'
    res.headers['Content-Disposition'] = 'attachment; filename='+ 'reservations' +'.csv'

    print(type(res))

    return res