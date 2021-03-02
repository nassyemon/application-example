import os
from flask import Blueprint, jsonify,request,redirect, url_for,flash,current_app
from application.models import Test

app = Blueprint('api', __name__)

@app.route('/')
def index():
    print("called index")
    return jsonify({
        "hello": "world!"
    })

@app.route('/__healthcheck')
def healthcheck():
    print("called healthcheck")
    return jsonify({
        "success": 1,
        "engine": "flask",
    })

@app.route('/__config')
def config():
    print("called healthcheck")
    return jsonify({
        'user': os.getenv('DB_USER', 'admin'),
        'password': os.getenv('DB_PASSWORD', 'simpway1'),
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '3306'),
        'dbname': os.getenv('DB_NAME', 'simpway'),
    })
