from datetime import datetime

from flask_login import UserMixin

from application.database import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    __table_args__ = (
        db.UniqueConstraint('name'),
        db.UniqueConstraint('email'),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15, collation='utf8mb4_general_ci'), nullable=False)
    display_name = db.Column(db.String(50, collation='utf8mb4_general_ci'), nullable=False)
    email = db.Column(db.String(256, collation='utf8mb4_general_ci'), nullable=False)
    password = db.Column(db.String(1024, collation='utf8mb4_general_ci'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __init__(self, name, display_name, email, password):
        self.name = name
        self.display_name = display_name
        self.email = email
        self.password = password

class Owner(db.Model, UserMixin):
    __tablename__ = 'owners'

    __table_args__ = (
        db.UniqueConstraint('name'),
        db.UniqueConstraint('email'),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15, collation='utf8mb4_general_ci'), nullable=False)
    display_name = db.Column(db.String(50, collation='utf8mb4_general_ci'), nullable=False)
    email = db.Column(db.String(256, collation='utf8mb4_general_ci'), nullable=False)
    password = db.Column(db.String(1024, collation='utf8mb4_general_ci'), nullable=False)
    start_hour = db.Column(db.String(50, collation='utf8mb4_general_ci'),nullable=True ,default=9)
    start_minites = db.Column(db.String(50, collation='utf8mb4_general_ci'),nullable=True ,default=0)
    end_hour = db.Column(db.String(50, collation='utf8mb4_general_ci'),nullable=True ,default=20)
    end_minites = db.Column(db.String(50, collation='utf8mb4_general_ci'),nullable=True ,default=0)
    master = db.Column(db.String(50, collation='utf8mb4_general_ci'),nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __init__(self, name, display_name, email, password,start_hour,start_minites,end_hour,end_minites):
        self.name = name
        self.display_name = display_name
        self.email = email
        self.password = password
        self.start_hour = start_hour
        self.start_minites = start_minites
        self.end_hour = end_hour
        self.end_minites = end_minites

class OwnerData(db.Model, UserMixin):
    __tablename__ = 'ownersData'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15, collation='utf8mb4_general_ci'), nullable=False)
    start_spot = db.Column(db.String(50, collation='utf8mb4_general_ci'), nullable=False)
    goal_spot = db.Column(db.String(50, collation='utf8mb4_general_ci'), nullable=False)
    car_class = db.Column(db.String(50, collation='utf8mb4_general_ci'), nullable=False)
    car_num = db.Column(db.String(50, collation='utf8mb4_general_ci'), nullable=False)
    child = db.Column(db.String(50, collation='utf8mb4_general_ci'), nullable=False)
    car_status = db.Column(db.String(50, collation='utf8mb4_general_ci'), nullable=True)
    display_status = db.Column(db.String(50, collation='utf8mb4_general_ci'), nullable=True)
    return_date =  db.Column(db.DateTime, nullable=True, default=datetime.now)
    display_date =  db.Column(db.DateTime, nullable=True, default=datetime.now)
    owner_delete_status = db.Column(db.String(50, collation='utf8mb4_general_ci'), nullable=True)
    nosmoke = db.Column(db.String(50, collation='utf8mb4_general_ci'), nullable=True)
    wd4 = db.Column(db.String(50, collation='utf8mb4_general_ci'), nullable=True)
    studless = db.Column(db.String(50, collation='utf8mb4_general_ci'), nullable=True)
    remarks = db.Column(db.String(250, collation='utf8mb4_general_ci'), nullable=True)

    # user info
    user_status = db.Column(db.String(50, collation='utf8mb4_general_ci'),nullable=True)
    user_name = db.Column(db.String(50, collation='utf8mb4_general_ci'),nullable=True)
    user_number = db.Column(db.String(50, collation='utf8mb4_general_ci'),nullable=True)
    user_mail = db.Column(db.String(50, collation='utf8mb4_general_ci'),nullable=True)
    user_check = db.Column(db.String(50, collation='utf8mb4_general_ci'),nullable=True)
    user_take_date =  db.Column(db.DateTime, nullable=True, default=datetime.now)
    user_return_date =  db.Column(db.DateTime, nullable=True, default=datetime.now)
    user_price = db.Column(db.String(50, collation='utf8mb4_general_ci'),nullable=True)
    user_remarks = db.Column(db.String(250, collation='utf8mb4_general_ci'), nullable=True)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __init__(
        self, 
        name,
        start_spot,
        goal_spot,
        car_class,
        car_num,
        child,
        car_status,
        nosmoke,
        wd4,
        studless,
        return_date,
        remarks,
        user_status,
        user_name,
        user_number,
        user_mail,
        user_check,
        display_status,
        display_date,
        user_take_date,
        user_return_date,
        owner_delete_status,
        user_price,
        user_remarks,
        updated_at,
        ):
        self.name = name
        self.start_spot = start_spot
        self.goal_spot = goal_spot
        self.car_class = car_class
        self.car_num = car_num
        self.child = child
        self.car_status = car_status
        self.nosmoke = nosmoke
        self.wd4 = wd4
        self.studless = studless
        self.return_date = return_date
        self.remarks = remarks
        self.user_status = user_status
        self.user_name = user_name
        self.user_number = user_number
        self.user_mail = user_mail
        self.user_check = user_check
        self.display_status = display_status
        self.display_date = display_date
        self.user_take_date = user_take_date
        self.user_return_date = user_return_date
        self.owner_delete_status = owner_delete_status
        self.user_price = user_price
        self.user_remarks = user_remarks
        self.updated_at = updated_at
