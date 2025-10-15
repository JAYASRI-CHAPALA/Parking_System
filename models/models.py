from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullname = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(300), nullable=True)
    role = db.Column(db.String(50), nullable=False, default='user')
    password = db.Column(db.String(150), nullable=False)
    

class ParkingLot(db.Model):
    __tablename__ = 'parking_lot'
    id = db.Column(db.String(20), primary_key = True )
    prime_location_name = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(300), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.String(10), nullable=False) 
    price =db.Column(db.Float, nullable=False)
    maximum_number_of_spots = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
class ParkingSpot(db.Model):
    __tablename__ = 'parking_spot'
    id = db.Column(db.String(20), primary_key=True)
    lot_id = db.Column(db.String(20), db.ForeignKey('parking_lot.id'), nullable=False)
    status = db.Column(db.String(10),nullable = False, default='A')
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    parking_lot = db.relationship('ParkingLot', backref=db.backref('spots', lazy=True))


class ReserveParkingSpot(db.Model):
    __tablename__ = 'reserve_parking_spot'
    id = db.Column(db.String(30) , primary_key = True)
    parkingcost = db.Column(db.Float, nullable=False)
    vehicle_number = db.Column(db.String(20), nullable=False)
    parking_timestamp = db.Column(db.DateTime, nullable=False , default= datetime.utcnow)
    leaving_timestamp = db.Column(db.DateTime, nullable=True)
    payment_status = db.Column(db.String(20), nullable=False, default='Pending')
    amount_paid = db.Column(db.Float, nullable=True)
    is_rated = db.Column(db.Boolean , nullable =True) 

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    spot_id = db.Column(db.String(20), db.ForeignKey('parking_spot.id'), nullable=False)  

    user = db.relationship('Users', backref='reservations')
    spot = db.relationship('ParkingSpot', backref='reservations')

class Rating(db.Model):
    __tablename__ = 'ratings'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lot_id = db.Column(db.String(20), db.ForeignKey('parking_lot.id'), nullable=False)
    
    rating = db.Column(db.Integer, nullable=False)  # 1 to 5
    
    user = db.relationship('Users', backref='given_ratings')
    parking_lot = db.relationship('ParkingLot', backref='received_ratings')
