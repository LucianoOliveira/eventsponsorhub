from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Users(db.Model, UserMixin):
    __tablename__ = 'tb_users'
    us_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    us_name = db.Column(db.String(50), nullable=False)
    us_email = db.Column(db.String(200))
    us_pwd = db.Column(db.String(150))
    us_birthday = db.Column(db.Date)
    us_is_buyer = db.Column(db.Boolean, default=True)
    us_is_seller = db.Column(db.Boolean, default=False)
    us_is_admin = db.Column(db.Boolean, default=False)
    us_is_superuser = db.Column(db.Boolean, default=False)
    us_is_active = db.Column(db.Boolean, default=True)

    def get_id(self):
        return str(self.us_id)

class Events(db.Model):
    __tablename__ = 'tb_events'
    ev_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ev_title = db.Column(db.String(100), nullable=False)
    ev_description = db.Column(db.String(500))
    ev_location = db.Column(db.String(200))
    ev_date = db.Column(db.DateTime, default=func.now())
    ev_expected_attendance = db.Column(db.Integer)
    ev_instagram = db.Column(db.String(200))
    ev_facebook = db.Column(db.String(200))
    ev_youtube = db.Column(db.String(200))
    ev_tiktok = db.Column(db.String(200))
    ev_user_id = db.Column(db.Integer, db.ForeignKey('tb_users.us_id'), nullable=False)
    ev_package_count = db.Column(db.Integer, default=0)
    ev_sold_package_count = db.Column(db.Integer, default=0)

    user = db.relationship('Users', backref=db.backref('events', lazy=True))

class Packages(db.Model):
    __tablename__ = 'tb_packages'
    pk_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pk_event_id = db.Column(db.Integer, db.ForeignKey('tb_events.ev_id'), nullable=False)
    pk_title = db.Column(db.String(100), nullable=False)
    pk_description = db.Column(db.String(500))
    pk_price = db.Column(db.Float, nullable=False)
    pk_is_sold = db.Column(db.Boolean, default=False)
    pk_allow_requests = db.Column(db.Boolean, default=False)
    pk_created_at = db.Column(db.DateTime, default=func.now())
    pk_user_id = db.Column(db.Integer, db.ForeignKey('tb_users.us_id'), nullable=False)

    event = db.relationship('Events', backref=db.backref('packages', lazy=True))
    user = db.relationship('Users', backref=db.backref('packages', lazy=True))

class UserRequests(db.Model):
    __tablename__ = 'tb_user_requests'
    ur_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ur_user_id = db.Column(db.Integer, db.ForeignKey('tb_users.us_id'), nullable=False)
    ur_request_type = db.Column(db.String(50), nullable=False)
    ur_request_time = db.Column(db.DateTime, default=func.now())
    ur_responded = db.Column(db.Boolean, default=False)
    ur_accepted = db.Column(db.Boolean, nullable=True)
    ur_response_time = db.Column(db.DateTime, nullable=True)
    ur_response_user_id = db.Column(db.Integer, db.ForeignKey('tb_users.us_id'), nullable=True)
    ur_response_reason = db.Column(db.String(500), nullable=True)

    user = db.relationship('Users', foreign_keys=[ur_user_id], backref=db.backref('requests', lazy=True))
    response_user = db.relationship('Users', foreign_keys=[ur_response_user_id], backref=db.backref('responses', lazy=True))


