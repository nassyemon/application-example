from typing import Text
import os
from os.path import join, dirname

from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


from application.models import User
from application.models import Owner
from application.models import OwnerData
from application.database import db

from . import user_mail

import datetime
import boto3
from dotenv import load_dotenv

auth = Blueprint('auth', __name__)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

REGION_NAME = os.environ.get('REGION_NAME')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
USER_POOL_ID = os.environ.get('USER_POOL_ID')
CLIENT_ID = os.environ.get('CLIENT_ID')

def cognito_get_user():
    try:
        aws_client = boto3.client('cognito-idp',
            region_name = REGION_NAME,
            aws_access_key_id = AWS_ACCESS_KEY_ID,
            aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
        )

        aws_result = aws_client.get_user(
            AccessToken=session['aws_cognito']["access_token"]
        )

        return aws_result

    except Exception as e:
        return None

def cognito_auth(user, passwd):
    try:
        aws_client = boto3.client('cognito-idp',
            region_name = REGION_NAME,
            aws_access_key_id = AWS_ACCESS_KEY_ID,
            aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
        )

        aws_result = aws_client.admin_initiate_auth(
            UserPoolId = USER_POOL_ID,
            ClientId = CLIENT_ID,
            AuthFlow = "ADMIN_USER_PASSWORD_AUTH",
            AuthParameters = {
                "USERNAME": user,
                "PASSWORD": passwd,
            }
        )
        return aws_result

    except:
        return None

def cognito_signout():
    aws_client = boto3.client('cognito-idp',
        region_name = REGION_NAME,
        aws_access_key_id = AWS_ACCESS_KEY_ID,
        aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    )
    aws_result = aws_client.admin_user_global_sign_out(
            UserPoolId = USER_POOL_ID,
            Username = session['aws_cognito']['user']
    )

    session.pop('aws_cognito', None)
    return None

def cognito_register_user(email,name,phone_number):
    try:
        aws_client = boto3.client('cognito-idp',
                                  region_name = REGION_NAME,
                                  aws_access_key_id = AWS_ACCESS_KEY_ID,
                                  aws_secret_access_key = AWS_SECRET_ACCESS_KEY,)

        response = aws_client.admin_create_user(
            UserPoolId=USER_POOL_ID,
            Username=email,
            UserAttributes=[
                {"Name": "email","Value": email},
                {"Name": "name","Value": name},
                {"Name": "phone_number","Value": phone_number},
                {"Name": "email_verified", "Value": "true" },
            ],
            DesiredDeliveryMediums=['EMAIL']
        )

        print("response=", response)

        return response
    except Exception as e:
        print(e)
    return None

def cognito_register_password(password):
    try:
        aws_client = boto3.client('cognito-idp',
            region_name = REGION_NAME,
            aws_access_key_id = AWS_ACCESS_KEY_ID,
            aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
        )

        response = aws_client.admin_respond_to_auth_challenge(
            UserPoolId=USER_POOL_ID,
            ClientId = CLIENT_ID,
            ChallengeName='NEW_PASSWORD_REQUIRED',
            ChallengeResponses={'USERNAME': session['aws_cognito']['user'], 'NEW_PASSWORD': password},
            Session=session['aws_cognito']['session']
        )
        print("response=", response)
        return response
    except Exception as e:
        print(e)
    return None

@auth.route('/login', methods=['GET'])
def login():
    return render_template('login.html', title='register mail', data=session)

@auth.route('/login', methods=['POST'])
def login_post():
    
    email = request.form['email']
    password = request.form['password']
    if email == '' or password == '':
        flash('メールアドレスまたはパスワードが空欄です')
        return redirect(url_for('auth.login'))

    if not 6 <= len(email) <= 254:
        flash('メールアドレスは 6 ~ 254 文字以内にして下さい')
        return redirect(url_for('auth.login'))

    if not 7 <= len(password):
        flash('パスワードは 7 文字以上です。')
        return redirect(url_for('auth.login'))

    aws_result = cognito_auth(email,password)
    if aws_result == None:
        flash('ユーザー名もしくはパスワードが間違っている可能性があります。')
        return redirect(url_for('auth.login'))
    elif 'ChallengeName' in aws_result and aws_result['ChallengeName'] == 'NEW_PASSWORD_REQUIRED':
        session["aws_cognito"] = {
        "user": email,
        "session": aws_result["Session"],
        "ChallengeParameters": aws_result["ChallengeParameters"],
        }
        return redirect(url_for('auth.password_change'))
    
    session["aws_cognito"] = {
        "user": email,
        "access_token": aws_result["AuthenticationResult"]["AccessToken"],
        "refresh_token": aws_result["AuthenticationResult"]["RefreshToken"]
    }

    if request.form.get('showid'):
        result = OwnerData.query.filter_by(id=request.form.get('showid')).first()
        display_day = result.display_date.date()
        return_day = result.return_date.date()
        return render_template('show.html', res=result, user=session['user'], display_day=display_day, return_day=return_day)


    return redirect(url_for('auth.profile'))

@auth.route('/signup', methods=['GET'])
def signup() -> Text:
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post() -> Text:
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        tel = request.form['tel']
        cognito_register_user(email,name,tel)

    return redirect(url_for('auth.login'))


@auth.route('/logout', methods=['GET'])
def logout():
    cognito_signout()
    return render_template('login.html', title='register mail', data=session)

@auth.route('/password', methods=["GET"])
def password_change():
    return render_template('password_reset.html',email=session['aws_cognito']["user"])

@auth.route('/password', methods=["POST"])
def password_change_post():
    password = request.form['password']
    cognito_register_password(password)
    return redirect(url_for('auth.login'))

@auth.route('/adduser', methods=['GET'])
def adduser():
    user_status = cognito_get_user()
    if user_status is None:
        flash('ログインをお願いします。')
    search_id = request.args.get("id")
    user_take_day = request.args.get("user_take_day")
    user_take_time = str(request.args.get("user_take_time"))
    user_return_day = request.args.get("user_return_day")
    user_return_time = str(request.args.get("user_return_time"))
    user_remarks = request.args.get("user_remarks")

    price = request.args.get("price")

    user_take_datetime = user_take_day + " " + user_take_time + ":00"
    user_return_datetime = user_return_day + " " + user_return_time + ":00"
    user_take_datetime = datetime.datetime.strptime(user_take_datetime,'%Y-%m-%d %H:%M:%S')
    user_return_datetime = datetime.datetime.strptime(user_return_datetime,'%Y-%m-%d %H:%M:%S')



    if not search_id == None:
        resister_car = OwnerData.query.filter_by(id=search_id).first()
        resister_car.user_mail = current_user.email
        resister_car.user_name = current_user.name
        resister_car.user_status = "あり"
        resister_car.user_return_date = user_return_datetime
        resister_car.user_take_date = user_take_datetime
        resister_car.user_check = '予約あり'
        resister_car.user_price = price
        resister_car.user_remarks = user_remarks
        try:
            db.session.add(resister_car)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
        finally:
            # user_mail.send_reserved(current_user.display_name,current_user.email,user_take_datetime,user_return_datetime,resister_car.start_spot,resister_car.goal_spot)
            db.session.close()
    return redirect(url_for('auth.profile'))

@auth.route('/profile', methods=['GET'])
def profile():
    user_status = cognito_get_user()
    if user_status is None:
        flash('ログインをお願いします。')
        return redirect(url_for('auth.login'))


    result = []
    # return render_template('profile.html', user=session['aws_cognito']['user'],result=result)
    return render_template('profile.html', user="あああ",result=result)

@auth.route('/cancel')
def car_cancel():
    user_status = cognito_get_user()
    if user_status is None:
        flash('ログインをお願いします。')

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


@auth.route('/check')
def check():
    user_status = cognito_get_user()
    print(type(user_status['UserAttributes']))
    return user_status['UserAttributes'][0]