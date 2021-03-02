from flask import Blueprint, jsonify,request,redirect, url_for,flash,current_app

app = Blueprint('main', __name__)

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
